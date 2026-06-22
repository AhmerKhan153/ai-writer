from agents.research.hackernews import get_hackernews_top_stories
from agents.research.topic_analyzer import analyze_trends
from agents.post_writer import create_post

def research_agent_node(state):
    stories = get_hackernews_top_stories()
    return {
        "stories": stories
    }

def topics_agent_node(state):
    stories = state["stories"]
    topics = analyze_trends(stories)
    return {
        "topics": topics
    }

def writer_agent_node(state):
    selected_topic = state["selected_topic"]
    post = create_post(selected_topic.Title)

    return {
        "selected_topic": selected_topic.Title,
        "post": post
    }

def approval_node(state):
    topics = state["topics"]
    print("Select the topic you want to write about:")
    for i, topic in enumerate(topics):
        print(f"{i + 1}. {topic.Title}")
    choice = int(input("Enter your choice (Press 0 to Reject) : "))

    if choice == 0:
        return {
            "approved": False
        }

    selected_topic = topics[choice - 1]

    return {
        "selected_topic": selected_topic.Title,
        "approved": True
    }
