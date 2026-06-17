from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:4b")

def create_post(topic):
    prompt = """You are a respected software architect.

    Create a LinkedIn post.

    Topic: {topic}

    Rules:

    - Maximum 150-250 words
    - Professional and practical tone
    - Human-like style
    - Contrarian if possible
    - Avoid generic AI buzzwords
    - Do not use emojis at the beginning of lines 
    - Do not use words like 'dive into,' 'delve,', 'The Truth?' or 'tapestry'"
    - Include discussion question at the end."""

    response = llm.invoke(prompt.format(topic=topic))
    return response.content