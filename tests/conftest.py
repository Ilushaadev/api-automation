# conftest.py
import pytest
import requests
from tests.utils.auth import auth_headers


@pytest.fixture()
def auth():
    """
    Provides authorization headers for API calls.
    Usage: pass `auth` into your test or helper.
    """
    return auth_headers()


@pytest.fixture()
def api_client(auth):
    """
    Provides a configured requests session with auth headers.
    Usage: api_client.get('/endpoint') or api_client.post('/endpoint', json=data)
    """
    session = requests.Session()
    session.headers.update(auth)
    session.timeout = 30
    return session


@pytest.fixture(autouse=True)
def setup_test_logging(caplog):
    """
    Automatically captures logs for all tests.
    Useful for debugging API responses and auth issues.
    """
    import logging
    caplog.set_level(logging.INFO)

