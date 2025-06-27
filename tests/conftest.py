# tests/conftest.py

import pytest
from litestar.testing import TestClient

from src.app import create_app
from src.storage.in_memory_db import InMemoryDB
from src.services.submission_service import SubmissionService
from src.services.search_service import SearchService

@pytest.fixture(scope="module")
def client() -> TestClient:
    test_db = InMemoryDB()
    test_submission_service = SubmissionService(db=test_db)
    test_search_service = SearchService(db=test_db)

    app = create_app(
        db_provider=lambda: test_db,
        submission_service_provider=lambda: test_submission_service,
        search_service_provider=lambda: test_search_service,
    )

    app.state["db"] = test_db

    return TestClient(app=app)
