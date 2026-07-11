from typing import Dict, Any, List


class TopicGeneration:
    def generate(self, stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {"title": story.get("title"), "url": story.get("url"), "insight": f"Write about {story.get('title')}"}
            for story in stories
        ]
