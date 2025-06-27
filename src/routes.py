from typing import Optional

from litestar import get, post
from litestar.response import Response

from src.domain.submit_request import SubmitRequest
from src.errors.base import ModelTypeError, NoItemsMatchedError
from src.services.search_service import SearchService
from src.services.submission_service import SubmissionService


@post("/submit")
async def submit_item(data: SubmitRequest, submission_service: SubmissionService) -> Response:
    try:
        id = submission_service.submit(data.value, data.tags)
    except ModelTypeError as e:
        return Response(status_code=400, content={"error": str(e)})
    return Response(status_code=201, content={"id": id})


@get("/data")
async def query_items(
        search_service: SearchService,
        value: str,
        tags: Optional[str] = None,
        limit: Optional[int] = None,
) -> Response:
    try:
        tag_list = tags.split(",") if tags else None
        data = search_service.search(value, tag_list, limit)
        return Response(status_code=200, content={"data": [item for item in data]})
    except NoItemsMatchedError as e:
        return Response(status_code=404, content={"error": str(e)})
