from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    stories: list[dict]
    topics: list
    selected_story: dict
    article: dict
    prompt: str
    draft: dict
    review_result: dict
    published: dict
    post: str
    approved: bool