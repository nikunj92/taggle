from litestar import Litestar

from src.storage.in_memory_db import init_state
from src.routes import submit_item, query_items

app = Litestar(
    route_handlers=[submit_item, query_items],
    on_startup=[init_state]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.src.main:app", host="127.0.0.1", port=8000, reload=True)
