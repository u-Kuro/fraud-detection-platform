def test_root_path():
    from fraud_detection_api.src.main import app
    assert any(route.path == "/" for route in app.routes)