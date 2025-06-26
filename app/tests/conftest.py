import pytest
from litestar.testing import TestClient
from app.src.main import app

@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app=app)
