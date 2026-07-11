from typing import Dict, Any


class TopicExtractor:
    """Standalone node that extracts a text prompt from cleaned article content."""

    def extract(self, cleaned_article: Dict[str, Any]) -> str:
        if not cleaned_article:
            return ""

        title = cleaned_article.get("title") or ""
        content = cleaned_article.get("content") or ""
        prompt = f"Write a concise topic summary for the article titled '{title}'.\n\n{content}"
        return prompt.strip()
