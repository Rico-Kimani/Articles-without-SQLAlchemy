import code
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def start():
    """
    Start an interactive Python console with pre-imported classes and get_connection().
    Useful for manual inspection and debugging.
    """
    banner = (
        "Interactive debugging console.\n"
        "Available objects:\n"
        "  - get_connection()\n"
        "  - Author, Article, Magazine\n"
    )
    namespace = globals().copy()
    namespace.update(locals())
    code.interact(banner=banner, local=namespace)

if __name__ == '__main__':
    start()
