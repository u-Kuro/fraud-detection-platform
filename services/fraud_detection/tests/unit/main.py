def test_root_path():
    from services.fraud_detection.src.main import app
    assert any(route.path == "/" for route in app.routes)