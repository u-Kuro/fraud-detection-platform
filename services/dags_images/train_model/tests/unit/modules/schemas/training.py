import pytest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from train_model.src.modules.schemas.training import TrainModelOutputs

class TestMLflowRegisteredModelInfo:
    @staticmethod
    @pytest.fixture
    def data() -> dict:
        return {
            "model": Pipeline(steps=[("passthrough", FunctionTransformer())]),
            "hyperparameters": {},
        }

    def test_values(self, data: dict):
        values = TrainModelOutputs(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            if isinstance(expected, dict):
                assert expected == actual
            else:
                assert expected is actual