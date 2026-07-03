from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    stories: list[dict]
    topics: list
    selected_story: dict
    article: dict
    post: str
    approved: bool