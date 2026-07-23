"""LLM post generation.

Returns the LinkedIn post body as plain text. Persistence and status are handled
by the orchestrator (see src/repository), NOT here, so a draft is only stored once
the caller decides to. The model is obtained from the central factory in src/llm.py.
"""

from src.llm import get_chat_model
from src.config import POST_WRITING_PROMPT_TEMPLATE, REWRITE_PROMPT_SUFFIX


def create_post(topic: str, is_rewrite: bool = False) -> str:
    prompt = POST_WRITING_PROMPT_TEMPLATE.format(topic=topic)
    if is_rewrite:
        prompt += REWRITE_PROMPT_SUFFIX

    response = get_chat_model().invoke(prompt)
    # LangChain chat models return a message object; fall back to str for safety.
    content = getattr(response, "content", response)
    return content if isinstance(content, str) else str(content)