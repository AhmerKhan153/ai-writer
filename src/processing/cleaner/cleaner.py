from typing import Dict, Any


class ArticleCleaner:
    """Standalone cleaner node for raw article data."""

    def clean(self, article: Dict[str, Any]) -> Dict[str, Any]:
        if not article or not isinstance(article, dict):
            return {}

        cleaned = {
            "title": article.get("title"),
            "url": article.get("url"),
            "content": article.get("articlehtml") or article.get("content") or "",
        }
        return cleaned
