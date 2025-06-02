from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def main():
    conn = get_connection()
    cursor = conn.cursor()

    # List all authors
    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    print("Authors:")
    for row in authors:
        print(f"- {row['id']}: {row['name']}")
    print()

    # List all magazines and their article titles
    cursor.execute("SELECT * FROM magazines")
    magazines = cursor.fetchall()
    print("Magazines and their articles:")
    for m in magazines:
        magazine = Magazine(
            id=m['id'],
            name=m['name'],
            category=m['category']
        )
        titles = magazine.article_titles()
        print(f"- {magazine.name} ({magazine.category}):")
        for title in titles:
            print(f"  * {title}")
    print()

    # Find the author with the most articles
    cursor.execute("""
        SELECT au.name, COUNT(ar.id) AS article_count
        FROM authors au
        JOIN articles ar ON au.id = ar.author_id
        GROUP BY au.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    top = cursor.fetchone()
    if top:
        print(f"Top author: {top['name']} with {top['article_count']} articles")
    conn.close()

if __name__ == '__main__':
    main()
