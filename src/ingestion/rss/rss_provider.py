from typing import Dict, List

from ingestion.article_provider import ArticleProvider


class RSSProvider(ArticleProvider):
    def fetch_top_articles(self, limit: int = 20) -> List[Dict[str, str]]:
        # Placeholder implementation; replace with real RSS parsing logic.
        return [
            {"title": f"RSS Story {i}", "url": f"https://rss.example/{i}"}
            for i in range(1, limit + 1)
        ]
