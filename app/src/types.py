from enum import Enum

class ValueType(str, Enum):
    HASH = "hash"
    DOMAIN = "domain"
    IP = "ip"
