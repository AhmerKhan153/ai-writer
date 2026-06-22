from typing import TypedDict

class WorkflowState(TypedDict):
    stories: list
    topics: list
    selected_topic: str
    post: str
    approved: bool