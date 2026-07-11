"""Standalone runner for HackerNews ingestion."""

from ingestion.hackernews.hn_ingestor import HackerNewsIngestor
from repository.article_repository import ArticleRepository


def main() -> None:
    provider = HackerNewsIngestor()
    articles = provider.fetch_top_articles(limit=10)
    repo = ArticleRepository(storage_dir="./data")
    path = repo.save_articles(articles)
    print(f"Saved {len(articles)} articles to {path}")


if __name__ == "__main__":
    main()
