from litestar import Litestar
from litestar.di import Provide

from src.dependencies import get_submission_service, get_search_service
from src.routes import submit_item, query_items
from src.storage import init_state

app = Litestar(
    route_handlers=[submit_item, query_items],
    on_startup=[init_state],
    dependencies={
        "submission_service": Provide(get_submission_service),
        "search_service": Provide(get_search_service),
    }
)


def main():
    import uvicorn
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
