def test_root_path():
    from services.fraud_detection_api.src.main import app
    assert any(route.path == "/" for route in app.routes)