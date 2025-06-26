
import pytest
from src.services.submission_service import SubmissionService
from src.storage.in_memory_db import InMemoryDB
from src.domain import ValueType
from src.errors.base import ModelTypeError


def test_submit_inserts_new_item():
    db = InMemoryDB()
    service = SubmissionService(db)
    value = "127.0.0.1"
    tags = ["foo", "bar"]

    item_id = service.submit(value, tags)
    stored = db.get_by_value(value)

    assert len(stored) == 1
    assert stored[0].id == item_id
    assert set(stored[0].tags) == {"foo", "bar"}
    assert stored[0].value == "127.0.0.1"
    assert stored[0].type == ValueType.IP


def test_submit_deduplicates_same_value_tags():
    db = InMemoryDB()
    service = SubmissionService(db)
    value = "127.0.0.1"
    tags = ["foo", "bar"]

    id1 = service.submit(value, tags)
    id2 = service.submit(value.upper(), ["BAR", "FOO"])  # reordered + cased

    assert id1 == id2
    assert len(db.get_by_value(value)) == 1


def test_submit_adds_if_tags_differ():
    db = InMemoryDB()
    service = SubmissionService(db)
    value = "127.0.0.1"

    id1 = service.submit(value, ["foo"])
    id2 = service.submit(value, ["foo", "bar"])

    assert id1 != id2
    assert len(db.get_by_value(value)) == 2


def test_invalid_value_raises():
    db = InMemoryDB()
    service = SubmissionService(db)

    with pytest.raises(ModelTypeError):
        service.submit("not-an-ip-or-hash", ["foo"])
