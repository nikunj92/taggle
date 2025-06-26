from typing import List, Optional

from pydantic import BaseModel


class SubmitRequest(BaseModel):
    value: str
    tags: Optional[List[str]] = []