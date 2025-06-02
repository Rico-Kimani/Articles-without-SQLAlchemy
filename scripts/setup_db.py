import sys
import os

# ✅ Fix: Add the root directory to Python path BEFORE importing from lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.connection import DB_PATH, get_connection

def setup_database():
    """
    Create the SQLite database file (if it doesn't exist) and
    execute schema.sql to create all tables.
    """
    # Ensure the directory for DB_PATH exists
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = get_connection()
    cursor = conn.cursor()

    # Read the SQL schema file
    script_dir = os.path.dirname(__file__)
    schema_path = os.path.join(script_dir, '..', 'lib', 'db', 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Database and tables created successfully.")

if __name__ == '__main__':
    setup_database()
