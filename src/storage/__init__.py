from litestar import Litestar

from src.storage.in_memory_db import InMemoryDB


def init_db(app: Litestar):
    app.state.db = InMemoryDB()