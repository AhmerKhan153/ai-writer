from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agents.topic_discovery import discover_topics
from agents.post_writer import create_post

topics = discover_topics()

print(topics)
print("\n Select a topic number to create a LinkedIn post:") 
topic = input()
try:    
    topic_index = int(topic) - 1
    if 0 <= topic_index < len(topics.splitlines()):
        selected_topic = topics.splitlines()[topic_index]
        post = create_post(selected_topic)
        print(f"\n Generated LinkedIn Post on topic '{selected_topic}':\n")
        print(post)
    else:
        print("Invalid topic number.")
except ValueError:
    print("Please enter a valid number.")
finally:    print("\n Process completed.")
    