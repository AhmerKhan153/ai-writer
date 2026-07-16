from typing import Dict, Any

from config import TOPIC_EXTRACTION_PROMPT_TEMPLATE


class TopicExtractor:
    """Standalone node that extracts a text prompt from cleaned article content."""

    def extract(self, cleaned_article: Dict[str, Any]) -> str:
        if not cleaned_article:
            return ""

        title = cleaned_article.get("title") or ""
        content = cleaned_article.get("content") or ""
        prompt = TOPIC_EXTRACTION_PROMPT_TEMPLATE.format(title=title, content=content)
        return prompt.strip()
