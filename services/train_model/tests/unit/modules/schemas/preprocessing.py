import numpy
import pytest
from sklearn.model_selection import StratifiedKFold

from services.train_model.src.modules.schemas.preprocessing import PreprocessOutputs

class TestPreprocessOutputs:
    @staticmethod
    @pytest.fixture
    def data() -> dict:
        return {
            "x_train": numpy.array([]),
            "x_test": numpy.array([]),
            "y_train": numpy.array([]),
            "y_test": numpy.array([]),
            "original_y_train_positive_scale": 1.0,
            "cross_validation": StratifiedKFold(),
        }

    def test_values(self, data: dict):
        values = PreprocessOutputs(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            if isinstance(expected, numpy.ndarray):
                numpy.array_equal(expected, actual)
            elif isinstance(expected, float):
                assert expected == pytest.approx(actual)
            elif isinstance(expected, StratifiedKFold):
                assert expected.n_splits == actual.n_splits
                assert expected.shuffle == actual.shuffle
            else:
                raise ValueError(f"Unexpected key: {key}")