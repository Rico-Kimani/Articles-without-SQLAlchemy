import sqlite3
import os

# Define the path to the SQLite database file (db.sqlite3) next to this file
DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

def get_connection():
    """
    Return a new SQLite connection with row factory set to sqlite3.Row
    so that queries return dict-like rows.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
