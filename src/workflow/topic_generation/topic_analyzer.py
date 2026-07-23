from typing import Dict, Any, List

from models.topics import TopicList
from src.llm import get_structured_llm
from config import TOPIC_ANALYSIS_PROMPT_TEMPLATE


def analyze_trends(stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    text = "\n".join(story.get("title", "") for story in stories)
    prompt = TOPIC_ANALYSIS_PROMPT_TEMPLATE.format(text=text)
    result = get_structured_llm(TopicList).invoke(prompt)
    return result.topics
