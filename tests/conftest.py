import pytest
from litestar.testing import TestClient
from src import app

@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app=app)
