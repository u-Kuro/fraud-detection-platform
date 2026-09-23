import pytest

from train_model.modules.schemas.mlflow import MLflowRegisteredModelInfo

class TestMLflowRegisteredModelInfo:
    @staticmethod
    @pytest.fixture
    def data() -> dict:
        return {
            "run_id": "value",
            "model_id": "value",
            "model_name": "value",
            "model_version": 1,
        }

    def test_values(self, data: dict):
        values = MLflowRegisteredModelInfo(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual