from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        """
        Insert a new article if self.id is None, otherwise update existing.
        After insertion, self.id is set to the last row ID.
        """
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(
                id=row['id'],
                title=row['title'],
                author_id=row['author_id'],
                magazine_id=row['magazine_id']
            )
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(
                id=row['id'],
                title=row['title'],
                author_id=row['author_id'],
                magazine_id=row['magazine_id']
            )
        return None

    @classmethod
    def find_by_author(cls, author):
        """
        Return a list of Article instances written by the given Author instance.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?",
            (author.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            cls(
                id=row['id'],
                title=row['title'],
                author_id=row['author_id'],
                magazine_id=row['magazine_id']
            )
            for row in rows
        ]

    @classmethod
    def find_by_magazine(cls, magazine):
        """
        Return a list of Article instances published in the given Magazine instance.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (magazine.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            cls(
                id=row['id'],
                title=row['title'],
                author_id=row['author_id'],
                magazine_id=row['magazine_id']
            )
            for row in rows
        ]
