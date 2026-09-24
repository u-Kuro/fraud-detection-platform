def test_root_path():
    from fraud_detection_api.main import app
    assert any(route.path == "/" for route in app.routes)