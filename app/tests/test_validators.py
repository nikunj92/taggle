from app.src.types import ValueType
from app.src.utils.validators import detect_item_type

def test_valid_ip():
    assert detect_item_type("8.8.8.8") is ValueType.IP
    assert detect_item_type("256.256.256.256") is ValueType.IP

def test_valid_hash():
    assert detect_item_type("aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d") is ValueType.HASH
