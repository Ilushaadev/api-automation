#tests for loging feature

import pytest
import requests
from tests.modules import login_function as login


def test_login_with_token():
    """
    Login with token

    1. verify access token is returned
    2. verify token type is returned
    3. verify token type is bearer
    4. verify expires default value
    """
    re = login.login()
    assert isinstance(re, dict)
    assert re.get("access_token")
    assert re.get("token_type") == "bearer"
    assert re.get("expires_in") == 7200


def test_login_with_incorrect_user():
    """
    Login with incorrect user

    1. verify error is raised
    2. verify error message is returned
    """
    invalid_creds = {
        "username": "test",
        "password": "test"
    }
    with pytest.raises(requests.HTTPError) as e:
         login.login(login_data=invalid_creds)
    status_code = e.value.response.status_code
    error_text = e.value.response.text

    assert status_code == 401
    assert "Invalid credentials" in error_text

