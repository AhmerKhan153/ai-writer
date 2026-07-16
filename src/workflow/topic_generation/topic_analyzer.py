from typing import Dict, Any, List

from models.topics import TopicList
from langchain_ollama import ChatOllama
from config import DEFAULT_LLM_MODEL, TOPIC_ANALYSIS_PROMPT_TEMPLATE

llm = ChatOllama(model=DEFAULT_LLM_MODEL)
structured_llm = llm.with_structured_output(TopicList)


def analyze_trends(stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    text = "\n".join(story.get("title", "") for story in stories)
    prompt = TOPIC_ANALYSIS_PROMPT_TEMPLATE.format(text=text)
    result = structured_llm.invoke(prompt)
    return result.topics
