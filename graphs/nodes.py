from agents.article_fetcher import fetch_article
from agents.research.hackernews import get_hackernews_top_stories
from agents.research.topic_analyzer import analyze_trends
from agents.post_writer import create_post


def research_agent_node(state):
    stories = get_hackernews_top_stories()
    return {"stories": stories}


# def topics_agent_node(state):
#     stories = state.get("stories", [])
#     topics = analyze_trends(stories)
#     return {"topics": topics}


def approval_node(state):
    stories = state.get("stories", [])

    if not stories:
        print("No stories were generated to approve.")
        return {"approved": False}

    print("Select the story you want to write about:")
    for index, story in enumerate(stories, start=1):
        title = getattr(story, "Title", None)
        if title is None and isinstance(story, dict):
            title = story.get("Title") or story.get("title")
        print(f"{index}. {title or str(story)}")

    try:
        choice = int(input("Enter your choice (Press 0 to reject): ").strip())
    except ValueError:
        return {"selected_story": {"approved": False}}

    if choice <= 0 or choice > len(stories):
        return {"selected_story": {"approved": False}}

    selected_story = stories[choice - 1]
    title = selected_story.get("Title") or selected_story.get("title")
    url = selected_story.get("url") or selected_story.get("URL")

    return {"selected_story": {"approved": True , "title": title , "url": url}}

def article_fetcher_node(state):
    selected_story = state["selected_story"]
    articlehtml = fetch_article(selected_story.get("url"))
    return {"article": { "title": selected_story.get("title"), "url": selected_story.get("url"), "articlehtml": articlehtml }}


def writer_agent_node(state):
    selected_story = state["article"]
    post = create_post(selected_story.get("articlehtml"))
    return {"selected_story": selected_story, "post": post}
