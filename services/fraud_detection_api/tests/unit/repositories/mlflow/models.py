import pytest

from fraud_detection_api.src.modules.schemas.mlflow import DeployedModel
from fraud_detection_api.src.repositories.mlflow.models import MlflowModel

class TestMlflowModel:
    @staticmethod
    @pytest.fixture
    def data():
        return {
            "deployed_model": DeployedModel(
                model_name="value",
                model_version=1
            )
        }

    def test_values(self, data: dict):
        values = MlflowModel(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual