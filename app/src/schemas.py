from typing import List, Optional

from pydantic import BaseModel

from app.src.types import ValueType


class SubmitRequest(BaseModel):
    value: str
    tags: Optional[List[str]] = []


class ItemResponse(BaseModel):
    value: str
    type: ValueType
    tags: List[str]
