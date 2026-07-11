import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.processing.cleaner.cleaner import ArticleCleaner
from src.processing.extractor.extractor import TopicExtractor
from src.processing.embeddings.embeddings import EmbeddingsGenerator


def test_article_cleaner_removes_none_values():
    cleaner = ArticleCleaner()
    cleaned = cleaner.clean({"title": "Test", "url": "http://example.com", "articlehtml": "Hello"})
    assert cleaned["title"] == "Test"
    assert cleaned["url"] == "http://example.com"
    assert cleaned["content"] == "Hello"


def test_topic_extractor_builds_prompt():
    extractor = TopicExtractor()
    prompt = extractor.extract({"title": "Test", "content": "Some article content."})
    assert "Write a concise topic summary" in prompt
    assert "Some article content." in prompt


def test_embeddings_generator_returns_embedding_structure():
    generator = EmbeddingsGenerator()
    embedding = generator.generate({"title": "Test", "url": "http://example.com", "content": "Hello"})
    assert embedding["title"] == "Test"
    assert embedding["content"] == "Hello"
    assert isinstance(embedding["embedding"], list)
