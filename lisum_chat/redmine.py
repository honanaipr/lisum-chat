from .config import config
import httpx
import json
import enum
from .schemas.redmine_schemas import SearchResponse


class FunctionType(enum.Enum):
    search = enum.auto()


async def request_json(function: FunctionType, query: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            config.redmine.url + "search.json",
            params={"q": query, "key": config.redmine.key},
        )
        return r.json()


async def search(query: str) -> SearchResponse:
    result = await request_json(FunctionType.search, query=query)
    return SearchResponse.model_validate(result)


json.load
