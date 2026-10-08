def test_health_path():
    from fraud_detection_api.main import app
    assert any(route.path == "/health" for route in app.routes)

def test_ready_path():
    from fraud_detection_api.main import app
    assert any(route.path == "/ready" for route in app.routes)