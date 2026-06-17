from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:4b")
def discover_topics():
    prompt = """Act as a principal software engineer.
    Suggest 10 LinkedIn post ideas.

    Requirements:

    - Advanced software architecture
    - AI engineering
    - Distributed systems
    - Contrarian opinions
    - Emerging technology

    Avoid beginner topics.
    Preferably mid to advance topics

    Return only a numbered list."""
    
    response = llm.invoke(prompt)
    return response.content