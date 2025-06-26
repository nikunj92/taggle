from litestar.datastructures import State

from src.services.search_service import SearchService
from src.services.submission_service import SubmissionService
from src.storage.in_memory_db import InMemoryDB


def get_submission_service(state: State) -> SubmissionService:
    db: InMemoryDB = state.db
    return SubmissionService(db)


def get_search_service(state: State) -> SearchService:
    db: InMemoryDB = state.db
    return SearchService(db)
