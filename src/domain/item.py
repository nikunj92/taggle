from dataclasses import field
from typing import List
from uuid import uuid4

from pydantic.dataclasses import dataclass

from src.domain import ValueType
from src.errors.base import ModelTypeError


@dataclass(frozen=True)
class StoredItem:
    id: str = field(default_factory=lambda: str(uuid4()))
    value: str = ""
    tags: List[str] = field(default_factory=list)
    type: ValueType = None

    def __post_init__(self):
        # Sanity checks to ensure that the service calling this model passed lower case values
        if self.value != self.value.lower():
            raise ModelTypeError("Model Value must be lowercase")

        if not all(tag == tag.lower() for tag in self.tags):
            raise ModelTypeError("All tags must be lowercase")

        if not isinstance(self.type, ValueType):
            raise ModelTypeError("Invalid type")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "value": self.value,
            "tags": self.tags,
            "type": self.type.value,
        }
