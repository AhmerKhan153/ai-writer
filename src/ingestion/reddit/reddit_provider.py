from typing import Dict, List

from ingestion.article_provider import ArticleProvider


class RedditProvider(ArticleProvider):
    def fetch_top_articles(self, limit: int = 20) -> List[Dict[str, str]]:
        # Placeholder implementation; replace with real Reddit API logic.
        return [
            {"title": f"Reddit Story {i}", "url": f"https://reddit.example/{i}"}
            for i in range(1, limit + 1)
        ]
