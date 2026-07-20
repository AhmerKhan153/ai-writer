import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import asyncio

from processing.fetcher.fetcher import fetch_article
from ingestion.provider_registry import registry
from ingestion.reddit.reddit_provider import RedditProvider
from ingestion.rss.rss_provider import RSSProvider
from ingestion.hackernews.hn_provider import HackerNewsProvider
from processing.cleaner.cleaner import ArticleCleaner
from processing.extractor.extractor import TopicExtractor
from workflow.topic_generation.topic_analyzer import analyze_trends
from workflow.writing.writing import WritingWorkflow
from workflow.reviewing.reviewing import ReviewingWorkflow
from workflow.publishing.publishing import PublishingWorkflow
from integration.telegram_bot import send_draft, send_story_selection
from integration.telegram_state import (
    create_pending_selection,
    get_pending_selection,
    set_selected_story,
)


def register_providers() -> None:
    registry.register("hackernews", HackerNewsProvider)
    registry.register("reddit", RedditProvider)
    registry.register("rss", RSSProvider)


register_providers()


def research_agent_node(state):
    provider_name = state.get("provider", "hackernews")
    if provider_name not in registry.list_providers():
        raise ValueError(f"Unknown provider: {provider_name}")

    provider_class = registry.get(provider_name)
    provider = provider_class()
    stories = provider.fetch_top_articles(limit=20)
    return {"stories": stories}


def topics_agent_node(state):
    stories = state.get("stories", [])
    topics = analyze_trends(stories)
    return {"topics": topics}


def approval_node(state):
    stories = state.get("stories", [])

    if not stories:
        print("No stories were generated to approve.")
        return {"selected_story": {"approved": False}}

    pending = get_pending_selection()
    if pending is None:
        pending = create_pending_selection(stories)
        options = []
        for index, story in enumerate(stories, start=1):
            title = getattr(story, "Title", None)
            if title is None and isinstance(story, dict):
                title = story.get("Title") or story.get("title")
            options.append(f"{index}. {title or str(story)}")

        try:
            asyncio.get_running_loop().create_task(
                send_story_selection(stories)
            )
        except RuntimeError:
            asyncio.run(send_story_selection(stories))

    if pending.selected_story is None:
        return {"selected_story": {"approved": False, "pending_selection": True, "stories": stories}}

    selected_story = pending.selected_story
    title = selected_story.get("title")
    url = selected_story.get("url")
    return {"selected_story": {"approved": True, "title": title, "url": url}}


def article_fetcher_node(state):
    selected_story = state["selected_story"]
    article_html = fetch_article(selected_story.get("url"))
    cleaned = ArticleCleaner().clean(
        {
            "title": selected_story.get("title"),
            "url": selected_story.get("url"),
            "articlehtml": article_html,
        }
    )
    prompt = TopicExtractor().extract(cleaned)
    return {"article": cleaned, "prompt": prompt}


def writer_agent_node(state):
    prompt = state.get("prompt", "")
    draft = WritingWorkflow().write(prompt)
    return {"draft": draft}


def review_node(state):
    draft = state.get("draft", {})
    review_result = ReviewingWorkflow().review(draft)
    return {"review_result": review_result}


def publish_node(state):
    review_result = state.get("review_result", {})
    published = PublishingWorkflow().publish(review_result)
    return {"published": published}
