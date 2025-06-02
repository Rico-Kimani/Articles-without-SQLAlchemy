import os
import pytest
from lib.db.connection import DB_PATH, get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

from scripts.setup_db import setup_database
from lib.db.seed import seed_data

@pytest.fixture(autouse=True)
def run_around_tests(tmp_path, monkeypatch):
    """
    Create a temporary SQLite database for each test, run schema + seed,
    then tear it down automatically when the test ends.
    """
    test_db = tmp_path / "test_db.sqlite3"
    monkeypatch.setattr('lib.db.connection.DB_PATH', str(test_db))
    setup_database()
    seed_data()
    yield
    # No explicit teardown needed; tmp_path is auto-cleaned.

def test_save_and_find_author():
    author = Author(name="Test Author")
    author.save()
    found = Author.find_by_name("Test Author")
    assert found is not None
    assert found.name == "Test Author"

def test_articles_and_magazines_relationship():
    # Seeded data includes "Alice Smith"
    author = Author.find_by_name("Alice Smith")
    articles = author.articles()
    assert len(articles) >= 1

    mags = author.magazines()
    assert len(mags) >= 1

    # Test add_article()
    mag = Magazine.find_by_name("Travel World")
    author.add_article(mag, "New Travel Article")
    updated_articles = author.articles()
    titles = [a['title'] for a in updated_articles]
    assert "New Travel Article" in titles

def test_topic_areas():
    author = Author.find_by_name("Alice Smith")
    topics = author.topic_areas()
    assert "Technology" in topics
