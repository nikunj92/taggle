from src import ValueType
from src.utils.helpers import detect_value_type

def test_valid_ip():
    assert detect_value_type("8.8.8.8") is ValueType.IP
    assert detect_value_type("255.255.255.255") is ValueType.IP

def test_valid_hash():
    assert detect_value_type("aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d") is ValueType.HASH

def test_valid_domain():
    assert detect_value_type("example.com") is ValueType.DOMAIN
    assert detect_value_type("sub.example.com") is ValueType.DOMAIN

def test_invalid_value():
    try:
        detect_value_type("invalid_value")
    except ValueError as e:
        assert str(e) == "Unsupported value: invalid_value! Did not match Domain, IP or Hash type"
    else:
        assert False, "Expected ValueError for invalid value"