#tests for service status

from tests.modules import service_health_function as service

def test_service_health():
    """
    Check service health status
    1. verify service message
    2. verify service status
    """
    resp = service.service_health()
    message = resp.get("message")
    status = resp.get("status")
    assert message == "Application is running"
    assert status == "healthy"