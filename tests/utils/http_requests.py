# tests/utils/http.py

import requests
from typing import Optional
from tests.utils.auth import auth_headers


def _request(method: str, url: str, body: Optional[dict] = None):
    """
    Internal helper for making an HTTP request with error handling and auth.
    """
    headers = auth_headers()
    res = requests.request(method, url, headers=headers, json=body)
    res.raise_for_status()
    return res.json()


def get_request(url, body: Optional[dict] = None):
    return _request("GET", url, body)


def post_request(url, body: Optional[dict] = None):
    return _request("POST", url, body)


def put_request(url, body: Optional[dict] = None):
    return _request("PUT", url, body)


def delete_request(url, body: Optional[dict] = None):
    return _request("DELETE", url, body)


def options_request(url, body: Optional[dict] = None):
    return _request("OPTIONS", url, body)