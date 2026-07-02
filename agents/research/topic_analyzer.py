from langchain_ollama import ChatOllama
from models.topics import TopicList

llm = ChatOllama(model="qwen3:4b")
structured_llm = llm.with_structured_output(TopicList)


def analyze_trends(stories):
    text = "\n".join(story.get("title", "") for story in stories)
    prompt = f"""
You are a principal architect.

These are current Hacker News discussions:

{text}

Identify:
1. Emerging themes
2. Under-discussed architecture topics
3. Contrarian viewpoints

Return 10 LinkedIn post ideas in structured JSON format.
"""
    result = structured_llm.invoke(prompt)
    return result.topics