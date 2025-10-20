# tests/utils/auth.py
import logging
import os
import requests
from dotenv import load_dotenv

from tests.endpoints.app_endpoints import Endpoints

load_dotenv()

API_USERNAME = os.getenv("ADMIN_USER")
API_PASSWORD = os.getenv("ADMIN_PASSWORD")
API_KEY = os.getenv("API_KEY")
AUTH_URL = Endpoints.AUTH



def auth_headers():
    """
    Returns authorization headers.
    If API_KEY is set, it will use API Key auth.
    Otherwise, it will attempt username/password authentication.
    """
    if API_KEY:
        logging.info("Using API Key authentication")
        return {"ApiKey": API_KEY}

    if not API_USERNAME or not API_PASSWORD:
        raise ValueError("Missing credentials: set API_KEY or ADMIN_USER/ADMIN_PASSWORD")

    try:
        response = requests.post(
            AUTH_URL,
            json={"username": API_USERNAME, "password": API_PASSWORD},
            timeout=10,
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise ValueError("No access_token in auth response")
        logging.info("Received JWT auth token")
        return {"Authorization": f"Bearer {token}"}
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to get auth token: {e}")
        raise