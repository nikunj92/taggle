from typing import Optional, List

from litestar import get, post
from litestar.datastructures import State
from litestar.response import Response

from src.errors.base import ValueTypeError
from src.domain.schemas import SubmitRequest, ItemResponse
from src.domain.types import ValueType
from src.utils.helpers import detect_value_type


@post("/submit")
async def submit_item(data: SubmitRequest, state: State) -> Response:
    try:
        value_type = detect_value_type(data.value)
    except ValueTypeError as e:
        return Response(status_code=400, content={"error": str(e)})
    return Response(status_code=201, content={"id": "generated-id"})


@get("/data")
async def query_items(
        value: Optional[str] = None,
        tags: Optional[str] = None,
        limit: Optional[int] = 10
) -> List[ItemResponse]:
    # TODO query after storage is implemented
    return [
        ItemResponse(
            value=value or "example.org",
            type=ValueType.HASH,
            tags=tags.split(",") if tags else [],
        )
    ]
