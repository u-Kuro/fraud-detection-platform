class TestPredictRouter:
    def test_prefix(self):
        from fraud_detection_api.src.controllers.routers.predict import router
        assert router.prefix == "/predict"

    def test_tags(self):
        from fraud_detection_api.src.controllers.routers.predict import router
        assert "predict" in router.tags