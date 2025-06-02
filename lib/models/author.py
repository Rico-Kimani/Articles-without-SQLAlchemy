from lib.db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        """
        Insert a new author if self.id is None, otherwise update existing.
        After insertion, self.id is set to the last row ID.
        """
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'])
        return None

    def articles(self):
        """
        Returns a list of sqlite3.Row objects for all articles written by this author.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?",
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def magazines(self):
        """
        Returns a list of sqlite3.Row objects for all distinct magazines
        this author has written for.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT m.*
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
            """,
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_article(self, magazine, title):
        """
        Create a new Article record linking this author to the given magazine.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, self.id, magazine.id)
        )
        conn.commit()
        conn.close()

    def topic_areas(self):
        """
        Returns a list of unique magazine categories this author has contributed to.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
            """,
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row['category'] for row in rows]
