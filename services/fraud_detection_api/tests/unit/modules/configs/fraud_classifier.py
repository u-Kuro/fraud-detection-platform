from fraud_detection_api.src.modules.configs.fraud_classifier import FraudClassifierConfig
from fraud_detection_api.src.modules.schemas.mlflow import DeployedModel

class TestFraudClassifierConfig:
    def test_values(self):
        assert isinstance(FraudClassifierConfig.classification_threshold, float)
        assert isinstance(FraudClassifierConfig.deployed_model, DeployedModel)

        assert 1.0 > FraudClassifierConfig.classification_threshold > 0.0