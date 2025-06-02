import sys
import os

# Add root path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear tables
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    # Seed authors
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Alice Smith",))   # ID 1
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("John Doe",))      # ID 2

    # Seed magazines
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Travel World", "Travel"))  # ID 1
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Today", "Technology"))  # ID 2

    # Seed articles
    # Alice writes for both Travel World and Tech Today
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                   ("Exploring Africa", 1, 1))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                   ("Latest Tech Trends", 1, 2))

    # John writes for Travel World
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                   ("Budget Travel Tips", 2, 1))

    conn.commit()
    conn.close()
    print("✅ Database seeded with complete test data.")

if __name__ == '__main__':
    seed_data()
