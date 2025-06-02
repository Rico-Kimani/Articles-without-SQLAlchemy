import pytest
from lib.db.connection import DB_PATH, get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

from scripts.setup_db import setup_database
from lib.db.seed import seed_data

@pytest.fixture(autouse=True)
def run_around_tests(tmp_path, monkeypatch):
    test_db = tmp_path / "test_db.sqlite3"
    monkeypatch.setattr('lib.db.connection.DB_PATH', str(test_db))
    setup_database()
    seed_data()
    yield

def test_save_and_find_article():
    author = Author.find_by_name("Alice Smith")
    mag = Magazine.find_by_name("Travel World")
    article = Article(title="Test Title", author_id=author.id, magazine_id=mag.id)
    article.save()
    found = Article.find_by_title("Test Title")
    assert found is not None
    assert found.title == "Test Title"

def test_find_by_author_and_magazine():
    author = Author.find_by_name("Alice Smith")
    author_articles = Article.find_by_author(author)
    assert isinstance(author_articles, list)
    assert len(author_articles) >= 1

    mag = Magazine.find_by_name("Tech Today")
    mag_articles = Article.find_by_magazine(mag)
    assert isinstance(mag_articles, list)
    assert len(mag_articles) >= 1
