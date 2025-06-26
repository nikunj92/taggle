from typing import Dict, List, Optional
from uuid import uuid4

from src.domain.types import ValueType
from src.errors.base import NoItemsMatchedError


class StoredItem:
    def __init__(self, value: str, tags: List[str], value_type: ValueType):
        self.id = str(uuid4())
        self.value = value.lower()
        self.tags = [tag.lower() for tag in tags]
        self.type = value_type

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "value": self.value,
            "tags": self.tags,
            "type": self.type.value,
        }


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
