from datetime import datetime, timezone
from uuid import uuid4, UUID

import pytest
from pytest_mock import MockerFixture

from fraud_detection_api.src.modules.configs.fraud_classifier import FraudClassifierConfig
from fraud_detection_api.src.modules.schemas.inferences.fraud_classification import FraudClassificationRequest
from fraud_detection_api.src.modules.schemas.mlflow import DeployedModel
from fraud_detection_api.src.repositories.mlflow.models import MlflowModel
from fraud_detection_api.src.services.fraud_classifier import FraudClassifier
from services_shared.src.modules.schemas.models_dataset.fraud_classification import FraudClassificationFeaturesKeys
from services_shared.src.modules.schemas.postgres.transaction_inferences import TransactionInferences

class TestFraudClassifier:
    @staticmethod
    @pytest.fixture
    def model_data() -> dict:
        return {
            "model_name": "value",
            "model_version": 1
        }

    @staticmethod
    @pytest.fixture
    def json_request() -> dict:
        return {
            TransactionInferences.transaction_id.key: str(uuid4()),
            FraudClassificationFeaturesKeys.transaction_timestamp: datetime.now().isoformat(),
            FraudClassificationFeaturesKeys.amount: 1.0,
            **{
                key: 1.0 for key in FraudClassificationFeaturesKeys
                if key.startswith("v") and key[1:].isdigit()
            },
        }

    def test_identity(self):
        assert issubclass(FraudClassifier, MlflowModel)

    def test_classify(
        self,
        mocker: MockerFixture,
        model_data: dict,
        json_request: dict,
    ):
        fraud_probability = 1.0

        fraud_classifier = FraudClassifier(deployed_model=DeployedModel(**model_data))
        mocker.patch.object(
            target=fraud_classifier.model,
            attribute="predict_proba",
            return_value=[[1.0 - fraud_probability, fraud_probability]]
        )
        output = fraud_classifier.classify(
            FraudClassificationRequest(**json_request)
        )

        for key, expected in model_data.items():
            actual = getattr(output, key)

            assert expected == actual

        for key, expected in json_request.items():
            actual = getattr(output, key)

            match key:
                case TransactionInferences.transaction_id.key:
                    assert UUID(expected) == actual
                case FraudClassificationFeaturesKeys.transaction_timestamp:
                    assert datetime.fromisoformat(expected).astimezone(timezone.utc) == actual
                case FraudClassificationFeaturesKeys.amount:
                    assert expected == pytest.approx(actual)
                case _ if key.startswith("v") and key[1:].isdigit():
                    assert expected == pytest.approx(actual)
                case _:
                    raise ValueError(f"Unexpected key: {key}")

        assert output.is_fraud is None
        assert output.is_fraud_probability == pytest.approx(fraud_probability)
        assert output.is_fraud_probability > FraudClassifierConfig.classification_threshold
