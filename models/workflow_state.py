from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    stories: list[dict]
    topics: list
    selected_topic: str
    post: str
    approved: bool