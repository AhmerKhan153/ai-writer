from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="qwen3:4b")

prompt = ChatPromptTemplate.from_template(
    """You are a senior software architect.

Generate a LinkedIn post about:

{topic}

Rules:

- Maximum 250 words
- Practical
- Human-like text
- Contrarian if possible
- Avoid generic AI buzzwords
- End with a discussion question"""
)

chain = prompt | llm
response = chain.invoke({"topic": "Why Modular monoliths are making a comeback?"})
print(response.content)

