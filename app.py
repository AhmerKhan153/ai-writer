from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agents.topic_discovery import discover_topics
from agents.post_writer import create_post
from agents.research.hackernews import get_hackernews_top_stories
from agents.research.topic_analyzer import analyze_trends

stories = get_hackernews_top_stories()
analysis = analyze_trends(stories)
for topic in analysis.topics:
    print(f"Title: {topic.Title}")
    print(f"Reason: {topic.Reason}")
    print(f"Description: {topic.description}")
    print(f"Popularity: {topic.Popularity}")
    print(f"Score: {topic.score}")
    print("-" * 40)
# news = get_hackernews_top_stories()
# print("Top Hacker News Stories:")
# for idx, story in enumerate(news, 1):
#     print(f"{idx}. {story['title']} (Score: {story['score']}, URL: {story['by']})")  
# topics = discover_topics()

# print(topics)
# print("\n Select a topic number to create a LinkedIn post:") 
# topic = input()
# try:    
#     topic_index = int(topic) - 1
#     if 0 <= topic_index < len(topics.splitlines()):
#         selected_topic = topics.splitlines()[topic_index]
#         post = create_post(selected_topic)
#         print(f"\n Generated LinkedIn Post on topic '{selected_topic}':\n")
#         print(post)
#     else:
#         print("Invalid topic number.")
# except ValueError:
#     print("Please enter a valid number.")
# finally:    print("\n Process completed.")
    