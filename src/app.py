# src/app.py

from litestar import Litestar
from litestar.di import Provide
from src.routes import submit_item, query_items

from src.dependencies import (
    get_submission_service,
    get_search_service,
    get_db,
)
from src.storage import init_db
from src.storage.in_memory_db import InMemoryDB


def create_app(
    *,
    db_provider=None,
    submission_service_provider=None,
    search_service_provider=None,
) -> Litestar:
    return Litestar(
        route_handlers=[submit_item, query_items],
        dependencies={
            "db": Provide(db_provider or get_db),
            "submission_service": Provide(submission_service_provider or get_submission_service),
            "search_service": Provide(search_service_provider or get_search_service),
        },
        on_startup=[init_db],
    )

app = create_app()


def main():
    import uvicorn
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
