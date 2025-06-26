from typing import List

from pydantic import BaseModel

from src.domain import ValueType


class DataResponse(BaseModel):
    value: str
    type: ValueType
    tags: List[str]
