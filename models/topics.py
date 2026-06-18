from pydantic import BaseModel

class TopicIdea(BaseModel):
    Title: str
    Reason: str
    description: str
    Popularity: str
    score: int

class TopicList(BaseModel):
    topics: list[TopicIdea]