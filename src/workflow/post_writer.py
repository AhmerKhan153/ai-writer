from typing import Any

from langchain_ollama import ChatOllama
from models.article_format import ArticleFormat
from shared.save import save_db
from config import DEFAULT_LLM_MODEL, POST_WRITING_PROMPT_TEMPLATE

llm = ChatOllama(model=DEFAULT_LLM_MODEL)
structured_llm = llm.with_structured_output(ArticleFormat)


def create_post(topic: str) -> Any:
    prompt = POST_WRITING_PROMPT_TEMPLATE
    response = structured_llm.invoke(prompt.format(topic=topic))
    save_db(response)
    return response
