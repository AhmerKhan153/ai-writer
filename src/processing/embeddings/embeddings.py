from typing import Dict, Any


class EmbeddingsGenerator:
    """Standalone embeddings node for cleaned article content."""

    def generate(self, cleaned_article: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": cleaned_article.get("title"),
            "url": cleaned_article.get("url"),
            "content": cleaned_article.get("content"),
            "embedding": [0.0],
        }
