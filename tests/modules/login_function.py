# tests/modules/login_function.py
from typing import Optional
from dotenv import load_dotenv
from tests.endpoints.app_endpoints import Endpoints
from tests.utils.http_requests import post_request
import os


# Endpoints
login_url = Endpoints.AUTH
load_dotenv()

#ENVS
API_USERNAME = os.getenv("ADMIN_USER")
API_PASSWORD = os.getenv("ADMIN_PASSWORD")
API_KEY = os.getenv("API_KEY")


def login(login_data: Optional[dict] = None, use_api_key: bool = False):
    """
    Login function with token or api key
    """
    if use_api_key:
        default_data = {
            "ApiKey": API_KEY
        }
    else:
        default_data = {
            "username": API_USERNAME,
            "password": API_PASSWORD
        }
    data = login_data or default_data
    re = post_request(login_url, data)
    return re