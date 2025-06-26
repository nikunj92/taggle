import pytest
from litestar.testing import TestClient

from src.app import app

@pytest.fixture(scope="module")
def client() -> TestClient:
    client = TestClient(app=app)
    client.app.on_startup[0](client.app) # make DI work
    return client
