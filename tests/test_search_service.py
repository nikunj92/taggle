
import pytest
from src.services.search_service import SearchService
from src.storage.in_memory_db import InMemoryDB, StoredItem
from src.domain import ValueType
from src.errors.base import NoItemsMatchedError


@pytest.fixture
def search_service() -> SearchService:
    db = InMemoryDB()
    # Prepopulate with two items
    db.insert(StoredItem(value="1.1.1.1", tags=["dns", "edge"], type=ValueType.IP))
    db.insert(StoredItem(value="1.1.1.1", tags=["infra"], type=ValueType.IP))
    db.insert(StoredItem(value="deadbeef", tags=["hash", "tag"], type=ValueType.HASH))
    return SearchService(db)


def test_search_matches_tags(search_service):
    result = search_service.search("1.1.1.1", tags=["dns"])
    assert len(result) == 1
    assert result[0].value == "1.1.1.1"
    assert "dns" in result[0].tags


def test_search_no_tag_filter(search_service):
    result = search_service.search("1.1.1.1")
    assert len(result) == 2


def test_search_tag_filter_multiple_results(search_service):
    result = search_service.search("1.1.1.1", tags=["dns", "infra"])
    assert len(result) == 2


def test_search_limit_applies(search_service):
    result = search_service.search("1.1.1.1", limit=1)
    assert len(result) == 1


def test_search_no_match_value(search_service):
    with pytest.raises(NoItemsMatchedError):
        search_service.search("8.8.8.8")


def test_search_no_match_tags(search_service):
    with pytest.raises(NoItemsMatchedError):
        search_service.search("1.1.1.1", tags=["nonexistent"])
