#module for testing service health

from tests.endpoints.app_endpoints import Endpoints
from tests.utils.http_requests import get_request
service_health_url = Endpoints.SERVICE_STATUS


def service_health():
    """
    get service app health status
    """
    re = get_request(service_health_url)
    return re