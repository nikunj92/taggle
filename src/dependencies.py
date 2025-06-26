from litestar.datastructures import State

from src.services.search_service import SearchService
from src.services.submission_service import SubmissionService
from src.storage.in_memory_db import InMemoryDB


async def get_submission_service(state: State) -> SubmissionService:
    return SubmissionService(await get_db(state))


async def get_search_service(state: State) -> SearchService:
    return SearchService(await get_db(state))

async def get_db(state: State) -> InMemoryDB:
    if not hasattr(state, "db"):
        raise Exception("Database not initialized in state. Ensure to set it before accessing. - name this exception something more descriptive")
    return state.db
