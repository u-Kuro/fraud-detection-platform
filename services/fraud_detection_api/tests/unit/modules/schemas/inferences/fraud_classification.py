from datetime import datetime, timezone
from uuid import uuid4, UUID

import pytest
from pydantic import ValidationError

from fraud_detection_api.src.modules.schemas.inferences.fraud_classification import FraudClassificationRequest, FraudClassificationResponse, FraudClassificationOutput
from fraud_detection_api.tests.unit.modules.schemas.mlflow import TestDeployedModel
from services_shared.src.modules.schemas.models_dataset.fraud_classification import FraudClassificationFeaturesKeys
from services_shared.src.modules.schemas.postgres.transaction_inferences import TransactionInferences

class TestFraudClassificationRequest:
    @staticmethod
    def make_request() -> dict:
        return {
            TransactionInferences.transaction_id.key: uuid4(),
            FraudClassificationFeaturesKeys.transaction_timestamp: datetime.now(),
            FraudClassificationFeaturesKeys.amount: 1.0,
            **{
                key: 1.0 for key in FraudClassificationFeaturesKeys
                if key.startswith("v") and key[1:].isdigit()
            },
        }

    @staticmethod
    def make_json_request(**overrides) -> dict:
        data = {
            TransactionInferences.transaction_id.key: str(uuid4()),
            FraudClassificationFeaturesKeys.transaction_timestamp: datetime.now().isoformat(),
            FraudClassificationFeaturesKeys.amount: 1.0,
            **{
                key: 1.0 for key in FraudClassificationFeaturesKeys
                if key.startswith("v") and key[1:].isdigit()
            },
        }
        data.update(overrides)
        return data

    def test_values(self):
        json_data = self.make_json_request()


        values = FraudClassificationRequest(**json_data)

        for key, expected in json_data.items():
            actual = getattr(values, key)

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

    def test_failure_for_extra_field(self):
        data = self.make_json_request(extra=0)
        with pytest.raises(ValidationError):
            FraudClassificationRequest(**data)

class TestFraudClassificationResponse:
    @staticmethod
    def make_response() -> dict:
        return {
            TransactionInferences.is_fraud_prediction.key: True,
            TransactionInferences.is_fraud_probability.key: 1.0
        }

    def test_values(self):
        data = self.make_response()
        values = FraudClassificationResponse(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            if isinstance(expected, float):
                assert expected == pytest.approx(actual)
            else:
                assert expected == actual

        assert 1.0 >= getattr(values, TransactionInferences.is_fraud_probability.key) >= 0.0

class TestFraudClassificationOutput:
    @staticmethod
    def make_output(**overrides) -> dict:
        data = {
            **TestFraudClassificationRequest.make_request(),
            **TestFraudClassificationResponse.make_response()
        }
        data.update(overrides)
        return data

    def test_values(self):
        model = TestDeployedModel.make_model()
        request = TestFraudClassificationRequest.make_request()
        response = TestFraudClassificationResponse.make_response()
        is_fraud = True

        values = FraudClassificationOutput(
            **model,
            **request,
            **response,
            is_fraud=is_fraud
        )

        for key, expected in model.items():
            actual = getattr(values, key)

            assert expected == actual

        for key, expected in (request | response).items():
            actual = getattr(values, key)

            if isinstance(expected, datetime):
                assert expected.astimezone(timezone.utc) == actual
            elif isinstance(expected, float):
                assert expected == pytest.approx(actual)
            else:
                assert expected == actual

        assert values.is_fraud == is_fraud