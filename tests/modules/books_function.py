# tests/modules/books_function.py
from typing import Optional
from tests.endpoints.app_endpoints import Endpoints
from tests.utils.http_requests import get_request, post_request

# Endpoints
get_books = Endpoints.GET_ALL_BOOKS
add_book = Endpoints.ADD_NEW_BOOK


def get_all_books():
    """
    Fetch all books.
    """
    return get_request(get_books)

def create_book(book_data: Optional[dict] = None):
    """
    Add a new book.
    If no book_data is provided, a default is used.
    """
    default_data = {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
    }
    data = book_data or default_data
    return post_request(add_book, data)