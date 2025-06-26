from litestar import Litestar

from src.storage.in_memory_db import InMemoryDB


def init_state(app: Litestar) -> None:
    app.state.db = InMemoryDB()
