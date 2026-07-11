from abc import ABC, abstractmethod
from typing import Dict, List


class ArticleProvider(ABC):
    """Base provider interface for article content sources."""

    @abstractmethod
    def fetch_top_articles(self, limit: int = 20) -> List[Dict[str, str]]:
        """Return top article metadata from the provider."""
        raise NotImplementedError()
