import re
from app.src.types import ValueType
from ipaddress import ip_address

# TODO test regexes are too strict or too loose or if libraries can be used
# TODO plug in to the app

HASH_REGEX = re.compile(r"^[a-fA-F0-9]{32,64}$")  # MD5/SHA1/SHA256
DOMAIN_REGEX = re.compile(
    r"^(?!-)([a-zA-Z0-9\-]{1,63}(?<!-)\.)+[a-zA-Z]{2,}$"
)

def detect_item_type(value: str) -> ValueType:
    try:
        ip_address(value)
        return ValueType.IP
    except ValueError:
        pass

    if HASH_REGEX.fullmatch(value):
        return ValueType.HASH

    if DOMAIN_REGEX.fullmatch(value):
        return ValueType.DOMAIN

    raise ValueError(f"Unrecognized value format: {value}")
