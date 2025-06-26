from typing import Optional, List

from litestar import get, post
from litestar.datastructures import State
from litestar.response import Response

from app.src.schemas import SubmitRequest, ItemResponse
from app.src.types import ValueType


@post("/submit")
async def submit_item(data: SubmitRequest, state: State) -> Response:
    # TODO design storage & validation
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
