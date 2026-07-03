from pydantic import BaseModel


class ArticleFormat(BaseModel):
    Description: str
    key_takeaways: str
    technologies: str
    problems_solved: list[str]
    trade-offs: list[str]
    interesting_quotes: list[str]
    potential_discussion_topics: list[str]