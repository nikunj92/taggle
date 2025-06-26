from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ValueType(str, Enum):
    HASH = "hash"
    DOMAIN = "domain"
    IP = "ip"

class SubmitRequest(BaseModel):
    value: str
    tags: Optional[List[str]] = []

class ItemResponse(BaseModel):
    value: str
    type: ValueType
    tags: List[str]

