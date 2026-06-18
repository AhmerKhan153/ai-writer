import requests

def get_hackernews_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(url).json()
    stories = []
    for story_id in ids[:20]:  # Get top 20 story IDs
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story = requests.get(story_url).json()
        if story.get("score") > 100:  # Filter stories with score greater than 100
            stories.append({
                "title": story.get("title"),
                "url": story.get("url"),
                "score": story.get("score"),
            })
    return stories

