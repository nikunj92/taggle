from litestar import Litestar

from src.storage.in_memory_db import init_state
from src.routes import submit_item, query_items

app = Litestar(
    route_handlers=[submit_item, query_items],
    on_startup=[init_state]
)

def main():
    import uvicorn
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()