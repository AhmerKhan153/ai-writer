from abc import ABC, abstractmethod
from typing import List, Dict


class Ingestor(ABC):
    """Generic ingestion interface for article sources."""

    @abstractmethod
    def fetch_top_articles(self, limit: int = 20) -> List[Dict[str, str]]:
        """Return top article metadata from the source."""
        raise NotImplementedError()
