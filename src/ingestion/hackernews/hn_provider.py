from typing import Dict, List

from ingestion.article_provider import ArticleProvider
import requests


def get_hackernews_top_stories() -> List[Dict[str, str]]:
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(url).json()
    stories = []
    for story_id in ids[:20]:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story = requests.get(story_url).json()
        if story.get("score", 0) > 100:
            stories.append({
                "title": story.get("title"),
                "url": story.get("url"),
                "score": story.get("score"),
            })
    return stories


class HackerNewsProvider(ArticleProvider):
    """Hacker News provider implementing the generic article provider interface."""

    def fetch_top_articles(self, limit: int = 20) -> List[Dict[str, str]]:
        stories = get_hackernews_top_stories() or []
        return stories[:limit] if limit else stories
