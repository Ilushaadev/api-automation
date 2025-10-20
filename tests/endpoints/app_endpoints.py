# src/api/endpoints.py
import os

from dotenv import load_dotenv

# Define the base URL for your API.
# This could be loaded from environment variables for different stages (dev, prod).
load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class Endpoints:
    """A class to hold all API endpoint paths."""

    # App Service Health
    SERVICE_STATUS = f"{BASE_URL}/health"

    # Authentication
    AUTH = f"{BASE_URL}/auth/login"


    # Books
    GET_ALL_BOOKS = f"{BASE_URL}/books/get_books"
    ADD_NEW_BOOK = f"{BASE_URL}/books/add_book"