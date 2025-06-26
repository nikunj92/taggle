# src/services/submission_service.py

from src.storage.in_memory_db import InMemoryDB, StoredItem
from src.utils.helpers import detect_value_type


class SubmissionService:
    def __init__(self, db: InMemoryDB):
        self.db = db

    def submit(self, value: str, tags: list[str]) -> str:
        value = value.lower()
        tags = [t.lower() for t in tags]
        value_type = detect_value_type(value)

        # check for duplicates TODO make more efficient - this is O(n^2) in the worst case
        existing = self.db.get_by_value(value)
        for item in existing:
            if set(item.tags) == set(tags):
                return item.id

        item = StoredItem(value=value, tags=tags, type=value_type)
        return self.db.insert(item)
