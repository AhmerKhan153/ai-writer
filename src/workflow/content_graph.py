"""LangGraph subgraph for the automated content stretch: fetch -> write.

It contains NO human-in-the-loop
node — approval and publishing are driven by Telegram callbacks (see
src/integration). Given a picked story it fetches + cleans the article, builds a
topic prompt, and produces a LinkedIn draft.
"""

from typing import TypedDict

from langgraph.graph import END, StateGraph

from processing.fetcher.fetcher import fetch_article
from processing.cleaner.cleaner import ArticleCleaner
from processing.extractor.extractor import TopicExtractor
from src.workflow.writing.writing import WritingWorkflow

# Cap article text fed to the LLM so prompts stay small for the local model.
_MAX_CONTENT_CHARS = 4000


class ContentState(TypedDict, total=False):
    title: str
    url: str
    is_rewrite: bool
    prompt: str
    draft: str


def _fetch_node(state: ContentState) -> dict:
    article_html = fetch_article(state.get("url")) or ""
    cleaned = ArticleCleaner().clean(
        {
            "title": state.get("title"),
            "url": state.get("url"),
            "articlehtml": article_html,
        }
    )
    cleaned["content"] = (cleaned.get("content") or "")[:_MAX_CONTENT_CHARS]
    prompt = TopicExtractor().extract(cleaned)
    # Fall back to the title alone if the article couldn't be fetched.
    return {"prompt": prompt or (state.get("title") or "")}


def _write_node(state: ContentState) -> dict:
    draft = WritingWorkflow().write(
        state.get("prompt", ""),
        is_rewrite=state.get("is_rewrite", False),
    )
    return {"draft": draft}


def _build_graph():
    builder = StateGraph(ContentState)
    builder.add_node("fetch", _fetch_node)
    builder.add_node("write", _write_node)
    builder.set_entry_point("fetch")
    builder.add_edge("fetch", "write")
    builder.add_edge("write", END)
    return builder.compile()


_graph = _build_graph()


def generate_draft(title: str, url: str, is_rewrite: bool = False) -> str:
    result = _graph.invoke(
        {"title": title, "url": url, "is_rewrite": is_rewrite}
    )
    return result.get("draft", "")
