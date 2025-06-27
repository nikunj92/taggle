from typing import List, Optional

from src.domain.data_response import DataResponse
from src.errors.base import NoItemsMatchedError, ModelTypeError
from src.storage.in_memory_db import InMemoryDB
from src.utils.helpers import detect_value_type


class SearchService:
    def __init__(self, db: InMemoryDB):
        self.db = db

    def search(self, value: str, tags: Optional[List[str]] = None, limit: Optional[int] = None) -> List[DataResponse]:
        value = value.lower()
        _ = detect_value_type(value)

        tags = [t.lower() for t in tags] if tags else None

        matches = self.db.get_by_value(value)

        if not matches:
            raise NoItemsMatchedError(f"No items found for value: {value}")

        filtered = []
        for item in matches:
            if not tags or any(tag in item.tags for tag in tags):
                filtered.append(item)
            if limit and len(filtered) >= limit:
                break

        if not filtered:
            raise NoItemsMatchedError(f"No items matched tag filter for value: {value}")

        return [DataResponse(value=item.value, type=item.type, tags=item.tags) for item in filtered]
