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
    selected_topic = state["topics"].topics[0]
    post = create_post(selected_topic.Title)

    return {
        "selected_topic": selected_topic.Title,
        "post": post
    }
