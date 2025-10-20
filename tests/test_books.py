#Tests for books feature

from tests.modules import books_function as books


def test_get_books():
    """
    Test get all books function
    1. verify response obj is dictionary
    2. verify books type is a list
    3. verify books list is not empty
    4. verify first title book is correct
    """
    response = books.get_all_books()
    assert isinstance(response, dict)
    assert isinstance(response["books"], list)
    assert len(response["books"]) > 0
    assert response["books"][0]["title"] == "The Great Gatsby"

def test_add_book():
    """
    Test add new book function
    1. verify book key is dict type
    2. verify books has at least one key
    3. verify book title is correct
    """
    response = books.create_book()
    book = response.get("book")
    book_title = book.get("title")
    assert isinstance(book, dict)
    assert len(book) > 0
    assert book_title == "Dune"

