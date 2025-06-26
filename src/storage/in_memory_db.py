from collections import defaultdict
from typing import Dict, List

from src.domain.item import StoredItem


class InMemoryDB:
    def __init__(self):
        self.items: Dict[str, StoredItem] = {}
        self.value_to_ids: Dict[str, List[str]] = defaultdict(list)

    # In a real world case, I would have mappers, but for an in memory store there are sufficient
    def insert(self, item: StoredItem) -> str:
        self.items[item.id] = item
        self.value_to_ids[item.value].append(item.id)
        return item.id

    def get_by_value(self, value: str) -> List[StoredItem]:
        value = value.lower()
        return [self.items[_id] for _id in self.value_to_ids[value]]
