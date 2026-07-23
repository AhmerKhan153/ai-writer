"""Scheduler jobs.

Two independent jobs, each a self-contained unit of work:

    source_news_job     -> fetch + rank stories, store them, send the pick list
    publish_approved_job -> post approved drafts to LinkedIn

The human decisions in between are handled by Telegram callbacks (telegram_handler).
"""

import asyncio

from ingestion.hackernews.hn_provider import HackerNewsProvider
from integration.telegram_bot import send_story_selection, send_text_message
from integration.linkedin_client import post_text, LinkedInError
from repository import draft_repository
from config import STATUS_POSTED

_STORIES_PER_CYCLE = 6


async def source_news_job() -> None:
    """Fetch ranked tech news, persist each story, and send the pick list."""
    print("Sourcing news...")

    stories = await asyncio.to_thread(
        HackerNewsProvider().fetch_top_articles, _STORIES_PER_CYCLE
    )
    if not stories:
        print("No stories sourced.")
        return

    for story in stories:
        story["id"] = await asyncio.to_thread(draft_repository.insert_sourced, story)

    await send_story_selection(stories)


async def publish_approved_job() -> None:
    """Post every approved draft to LinkedIn, then mark it posted."""
    approved = await asyncio.to_thread(draft_repository.find_approved)
    for record in approved:
        draft = record.get("draft") or ""
        try:
            url = await asyncio.to_thread(post_text, draft)
        except LinkedInError as exc:
            print(f"LinkedIn post failed for {record['id']}: {exc}")
            await send_text_message(f"⚠️ LinkedIn post failed: {exc}")
            continue

        await asyncio.to_thread(
            draft_repository.set_status, record["id"], STATUS_POSTED, linkedin_url=url
        )
        await send_text_message(f"🚀 Posted to LinkedIn: {url}")
