import pytest
import logging

from tests import get_url
from app.models.bible import BookTypeEnum


logger = logging.getLogger(__name__)

pytest.BASE_URL = "bible"


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "message" : "Hello Saimon !"}
    

def test_search_bible(client):
    # check default mg bible is in db    
    data = get_url(client, "search/")    
    default_bible = [b for b in data.results if b.version == "MG1886"]
    assert len(default_bible) > 0
    assert default_bible[0].lang.code == "mg"
    
    # check no result for fake lang and version
    data = get_url(client, "search/?lang=xx&version=grigri", check_empty=False)
    assert data.results == []
    
def test_search_books(client):
    data = get_url(client, "search/?lang=mg&version=MG1886")    
    bible_id = data.results[0].id
    
    data = get_url(client, f"{bible_id}/books?max_results=5&book_type={BookTypeEnum.NEW.value}")
    assert len(data.results) == 5
    book = data.results[-1]
    assert book.short_name == "ASA"
    assert book.chapter_count == 28
    
    
def test_get_verse(client):
    data = get_url(client, "verses/66/15?from_verse=1&to_chapter=17&to_verse=3")    
    first_verse = data.results[0]
    assert first_verse.chapter_rank == 15
    assert first_verse.subtitle is not None
    assert first_verse.rank == 1    
    last_verse = data.results[-1]
    assert last_verse.chapter_rank == 17
    assert last_verse.rank == 3
    assert any(verse.chapter_rank == 16 for verse in data.results)
    
    data = get_url(client, "verses/19/93?from_verse=2&to_verse=4")
    assert len(data.results) == 3
    first_verse = data.results[0]
    assert first_verse.chapter_rank == 93
    assert first_verse.book_rank == 19
    assert first_verse.subtitle is None
    assert first_verse.rank == 2
    last_verse = data.results[-1]
    assert last_verse.rank == 4
    assert last_verse.chapter_rank == 93
    assert last_verse.book_rank == 19
    
    data = get_url(client, "verses/19/91?from_verse=1", check_empty=False)
    assert len(data.results) == 16
    
    data = get_url(client, "verses/19/91?from_verse=1&to_chapter=93")
    assert len(data.results) == 36
    
    data = get_url(client, "verses/19/91?from_verse=2&to_chapter=94&to_verse=3")
    assert len(data.results) == 38
    
    # across different books
    data = get_url(client, "verses/40/28?from_verse=2&to_book=41&to_chapter=2&to_verse=5")
    assert len(data.results) == 69
    
    # new testament from Mat to Apo
    data = get_url(client, "verses/40/1?from_verse=1&to_book=66")       
    assert len(data.results) == 7958
    
    
    
    
    
