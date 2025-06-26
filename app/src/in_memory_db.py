from litestar import Litestar


def init_state(app: Litestar) -> None:
    app.state.db = {}  # TODO design in-memory store for fast access (query and insert)
