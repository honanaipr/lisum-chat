from pydantic import BaseModel
from datetime import datetime


class SearchResult(BaseModel):
    id: int
    title: str
    type: str
    url: str
    description: str
    datetime: datetime


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total_count: int | None
    offset: int
    limit: int
