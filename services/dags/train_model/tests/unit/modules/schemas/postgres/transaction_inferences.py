from datetime import datetime

import pytest
from pandas import DataFrame

from services.dags.train_model.src.modules.schemas.postgres.transaction_inferences import TransactionInferencesDatasetNow

class TestTransactionInferencesDatasetNow:
    @staticmethod
    @pytest.fixture
    def data() -> dict:
        return {
            "dataset": DataFrame(),
            "retrieved_iso_datetime": datetime.now().isoformat(),
        }

    def test_values(self, data: dict):
        values = TransactionInferencesDatasetNow(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            if isinstance(expected, DataFrame):
                assert expected.equals(actual)
            else:
                assert expected == actual