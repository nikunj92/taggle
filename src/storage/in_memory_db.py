from typing import Dict, List, Optional

from litestar import Litestar

from src.domain.item import StoredItem
from src.errors.base import NoItemsMatchedError

def init_state(app: Litestar) -> None:
    app.state.db = InMemoryDB()

class InMemoryDB:
    def __init__(self):
        self.items: Dict[str, StoredItem] = {}

    # In a real world case, I would have mappers, but for a in memory store there are sufficient
    def insert(self, item: StoredItem) -> str:
        self.items[item.value] = item
        return item.id

    def get_by_value(self, value: str) -> StoredItem:
        value = value.lower()
        return self.items[value]

    # TODO move this out of here - Maybe over engineering but for extensibility and serepation of concerns, should go in a service
    def search(self, value: str, tags: Optional[List[str]] = None, limit: Optional[int] = 10) -> List[StoredItem]:
        value = value.lower()
        item = self.get_by_value(value)
        if not item:
            raise NoItemsMatchedError(f'{value} not present in store.')
        item_tags = item.tags
        if set(item_tags) & set(tags):
            return [item]
        raise NoItemsMatchedError(f'{value} has {item_tags}. None matched with {tags}')
