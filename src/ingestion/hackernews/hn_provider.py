from typing import Dict, List

import requests

from ingestion.article_provider import ArticleProvider

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

# How many top ids to inspect before ranking. Bigger = better ranking, slower.
_SCAN_LIMIT = 50


def _fetch_item(story_id: int) -> Dict:
    try:
        return requests.get(ITEM_URL.format(story_id=story_id), timeout=10).json() or {}
    except requests.RequestException:
        return {}


def _rank_score(story: Dict) -> float:
    """Blend upvotes and discussion volume so 'talked-about' stories rank well."""
    return story.get("score", 0) + 2 * story.get("descendants", 0)


def get_hackernews_top_stories(limit: int = 8) -> List[Dict[str, object]]:
    try:
        ids = requests.get(TOP_STORIES_URL, timeout=10).json() or []
    except requests.RequestException:
        return []

    candidates = []
    for story_id in ids[:_SCAN_LIMIT]:
        story = _fetch_item(story_id)
        url = story.get("url")
        # Skip Ask HN / self-posts (no external url to fetch) and low-signal items.
        if not url or story.get("score", 0) < 50:
            continue
        candidates.append(
            {
                "title": story.get("title"),
                "url": url,
                "score": story.get("score", 0),
                "comments": story.get("descendants", 0),
            }
        )

    candidates.sort(key=_rank_score, reverse=True)
    return candidates[:limit]


class HackerNewsProvider(ArticleProvider):
    """Hacker News provider implementing the generic article provider interface."""

    def fetch_top_articles(self, limit: int = 8) -> List[Dict[str, object]]:
        return get_hackernews_top_stories(limit=limit)
