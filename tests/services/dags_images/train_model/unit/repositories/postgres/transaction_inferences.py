import copy
from datetime import datetime, timezone

import pandas
from pandas import DataFrame
from pytest_mock import MockerFixture

from shared.modules.configs.dataset import DatasetConfig
from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences
from train_model.repositories.postgres.transaction_inferences import get_timed_latest_unused_dataset

def test_get_timed_latest_unused_dataset(mocker: MockerFixture):
    dataframe = DataFrame({
        TransactionInferences.is_fraud.key: [1],
        TransactionInferences.is_fraud_prediction.key: [1],
        TransactionInferences.transaction_timestamp.key: [datetime.now(tz=timezone.utc)],
    })
    original_dataframe = copy.deepcopy(dataframe)
    mocker.patch(
        target="train_model.repositories.postgres.transaction_inferences.pandas.read_sql",
        return_value=dataframe
    )

    mocker.patch.object(
        target=DatasetConfig,
        attribute="minimum_rows",
        new=len(dataframe.index)
    )

    result = get_timed_latest_unused_dataset()
    original_dataframe[TransactionInferences.transaction_timestamp.key] = original_dataframe[TransactionInferences.transaction_timestamp.key].astype("datetime64[s, UTC]").astype("int64")

    pandas.testing.assert_frame_equal(result.dataset, original_dataframe)