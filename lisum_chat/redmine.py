from .config import config
import httpx
import json
import enum
import typing
from .schemas.redmine_schemas import SearchResponse


class FunctionType(enum.Enum):
    search = enum.auto()


def request_json(function: FunctionType, query: str) -> typing.Any:
    r = httpx.get(
        config.redmine.url + "search.json",
        params={"q": query, "key": config.redmine.key},
    )
    return r.json()


def search(query: str) -> SearchResponse:
    result = request_json(FunctionType.search, query=query)
    return SearchResponse.model_validate(result)


json.load
