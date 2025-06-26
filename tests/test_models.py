from src.domain import ValueType
from src.domain.data_response import DataResponse
from src.domain.submit_request import SubmitRequest


def test_submit_schema_defaults():
    model = SubmitRequest(value="1.2.3.4")
    assert model.value == "1.2.3.4"
    assert model.tags == []

def test_response_schema():
    item = DataResponse(value="deadbeef", tags=["tag1"], type=ValueType.HASH)
    assert dict(item)["type"] == ValueType.HASH
