"""Central LLM factory.

Single seam for the whole app's language model. Today it returns a local
Ollama model; switching to Claude later is a one-line change here plus setting
ANTHROPIC_API_KEY in the environment. Nothing else in the codebase instantiates
a chat model directly.
"""

from typing import Any, Optional, Type

try:
    from src.config import DEFAULT_LLM_MODEL, LLM_PROVIDER, CLAUDE_MODEL
except ImportError:  # pragma: no cover - fallback for direct script execution
    from config import DEFAULT_LLM_MODEL, LLM_PROVIDER, CLAUDE_MODEL


def get_chat_model() -> Any:
    """Return a bare chat model for the configured provider."""
    if LLM_PROVIDER == "claude":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=CLAUDE_MODEL, temperature=0.7)

    # default: local Ollama
    from langchain_ollama import ChatOllama

    return ChatOllama(model=DEFAULT_LLM_MODEL)


def get_structured_llm(schema: Type) -> Any:
    """Return a chat model that emits validated instances of ``schema``."""
    return get_chat_model().with_structured_output(schema)