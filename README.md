### Project Overview.
This  project is a small console-based app written in Python, designed to model a basic magazine publishing system. It includes Authors, Articles and Magazines. 
It uses a local SQLite database to store data as well as retrive it. It emphasizes on organization using Object-Oriented Programming Principles.

### Project Structure
The project is structured into the following modules:
- `models.py`: This module contains classes representing Authors, Articles and Magazines. 
- `database.py`: This module contains functions to interact with the SQLite database, database schema and seed data.
- `Scripts/`: This has a script that sets up the database.
- `tests`: Contains test files to check correct working functionality
- `README.md`: File explains how the project works. (You are reading it now).

### Getting started
1. Clone the repository.
2. Set Up Your Python Environment.
3. Install the required packages by running `pip install -r requirements.txt`
4. Run `python Scripts/setup_db.py` to create the database.
5. Add some starter data by running `python lib/db/seed.py`.
6. Run the test by running `pytest`.


### Using the App
The models(Author, Article, Magazine)  interact with the SQLite database via custom class methods.

You can import this models into a python shell to dirrectly interact 

    `from lib.models.author import Author`
    `from lib.models.article import Article`
    `from lib.models.magazine import Magazine`

#Example: Find author by name
`author = Author.find_by_name("John Doe")`
`print(author.name)`

#Example: Create new article
`new_article = Article(title="Python & SQLite", author_id=1, magazine_id=2)`
`new_article.save()`