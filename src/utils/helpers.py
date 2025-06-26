import re
from ipaddress import ip_address

from src.domain import ValueType
from src.errors.base import ModelTypeError

# TODO test regexes are too strict or too loose or if libraries can be used

HASH_REGEX = re.compile(r"^[a-fA-F0-9]{32,64}$")  # MD5/SHA1/SHA256
DOMAIN_REGEX = re.compile(
    r"^(?!-)([a-zA-Z0-9\-]{1,63}(?<!-)\.)+[a-zA-Z]{2,}$"
)


def detect_value_type(value: str) -> ValueType:
    if HASH_REGEX.fullmatch(value):
        return ValueType.HASH

    if DOMAIN_REGEX.fullmatch(value):
        return ValueType.DOMAIN

    try:
        ip_address(value)
        return ValueType.IP
    except ValueError:
        raise ModelTypeError(f"Unsupported value: {value}! Did not match Domain, IP or Hash type")
