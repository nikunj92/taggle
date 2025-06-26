from app.src.schemas import SubmitRequest, ItemResponse
from app.src.types import ValueType


def test_submit_schema_defaults():
    model = SubmitRequest(value="1.2.3.4")
    assert model.value == "1.2.3.4"
    assert model.tags == []

def test_response_schema():
    item = ItemResponse(value="deadbeef", tags=["tag1"], type=ValueType.HASH)
    assert dict(item)["type"] == ValueType.HASH
