from typing import Optional, List

from litestar import get, post
from litestar.datastructures import State
from litestar.response import Response


from src.domain import ValueType
from src.domain.data_response import DataResponse
from src.domain.submit_request import SubmitRequest
from src.errors.base import ModelTypeError
from src.utils.helpers import detect_value_type


@post("/submit")
async def submit_item(data: SubmitRequest, state: State) -> Response:
    try:
        value_type = detect_value_type(data.value)
    except ModelTypeError as e:
        return Response(status_code=400, content={"error": str(e)})
    return Response(status_code=201, content={"id": "generated-id"})


@get("/data")
async def query_items(
        value: Optional[str] = None,
        tags: Optional[str] = None,
        limit: Optional[int] = 10
) -> List[DataResponse]:
    # TODO query after storage is implemented
    return [
        DataResponse(
            value=value or "example.org",
            type=ValueType.HASH,
            tags=tags.split(",") if tags else [],
        )
    ]
