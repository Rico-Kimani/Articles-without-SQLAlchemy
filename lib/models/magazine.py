from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        """
        Insert a new magazine if self.id is None, otherwise update existing.
        After insertion, self.id is set to the last row ID.
        """
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row['id'], name=row['name'], category=row['category'])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [
            cls(id=row['id'], name=row['name'], category=row['category'])
            for row in rows
        ]

    def articles(self):
        """
        Returns a list of sqlite3.Row objects for all articles in this magazine.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def contributors(self):
        """
        Returns a list of sqlite3.Row objects representing all distinct authors
        who have written for this magazine.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT au.*
            FROM authors au
            JOIN articles ar ON au.id = ar.author_id
            WHERE ar.magazine_id = ?
            """,
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def article_titles(self):
        """
        Returns a list of titles (strings) for all articles in this magazine.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title FROM articles WHERE magazine_id = ?",
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row['title'] for row in rows]

    def contributing_authors(self):
        """
        Returns a list of sqlite3.Row objects for authors with >2 articles in this magazine.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT au.*, COUNT(ar.id) AS article_count
            FROM authors au
            JOIN articles ar ON au.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY au.id
            HAVING article_count > 2
            """,
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
