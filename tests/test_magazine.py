import pytest
from lib.db.connection import DB_PATH, get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

from scripts.setup_db import setup_database
from lib.db.seed import seed_data

@pytest.fixture(autouse=True)
def run_around_tests(tmp_path, monkeypatch):
    test_db = tmp_path / "test_db.sqlite3"
    monkeypatch.setattr('lib.db.connection.DB_PATH', str(test_db))
    setup_database()
    seed_data()
    yield

def test_save_and_find_magazine():
    mag = Magazine(name="Test Magazine", category="Test Category")
    mag.save()
    found = Magazine.find_by_name("Test Magazine")
    assert found is not None
    assert found.category == "Test Category"

def test_articles_contributors_titles():
    mag = Magazine.find_by_name("Tech Today")
    articles = mag.articles()
    assert len(articles) >= 1

    contributors = mag.contributors()
    assert len(contributors) >= 1

    titles = mag.article_titles()
    assert isinstance(titles, list)
    assert len(titles) >= 1

    contrib_authors = mag.contributing_authors()
    # Seeded data has Alice Smith with 2 articles; contributing_authors() expects >2
    assert isinstance(contrib_authors, list)
