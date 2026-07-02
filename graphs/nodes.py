from agents.research.hackernews import get_hackernews_top_stories
from agents.research.topic_analyzer import analyze_trends
from agents.post_writer import create_post


def research_agent_node(state):
    stories = get_hackernews_top_stories()
    return {"stories": stories}


def topics_agent_node(state):
    stories = state.get("stories", [])
    topics = analyze_trends(stories)
    return {"topics": topics}


def approval_node(state):
    topics = state.get("topics", [])

    if not topics:
        print("No topics were generated to approve.")
        return {"approved": False}

    print("Select the topic you want to write about:")
    for index, topic in enumerate(topics, start=1):
        title = getattr(topic, "Title", None)
        if title is None and isinstance(topic, dict):
            title = topic.get("Title") or topic.get("title")
        print(f"{index}. {title or str(topic)}")

    try:
        choice = int(input("Enter your choice (Press 0 to reject): ").strip())
    except ValueError:
        return {"approved": False}

    if choice <= 0 or choice > len(topics):
        return {"approved": False}

    selected_topic = topics[choice - 1]
    title = getattr(selected_topic, "Title", None)
    if title is None and isinstance(selected_topic, dict):
        title = selected_topic.get("Title") or selected_topic.get("title")

    return {"selected_topic": title or str(selected_topic), "approved": True}


def writer_agent_node(state):
    selected_topic = state["selected_topic"]
    post = create_post(selected_topic)
    return {"selected_topic": selected_topic, "post": post}
