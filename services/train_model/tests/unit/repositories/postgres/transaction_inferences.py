from datetime import datetime

import pandas
from pandas import DataFrame
from pytest_mock import MockerFixture

from services.shared.src.modules.configs.dataset import DatasetConfig
from services.shared.src.modules.schemas.postgres.transaction_inferences import TransactionInferences
from services.train_model.src.repositories.postgres.transaction_inferences import get_timed_latest_unused_dataset

def test_get_timed_latest_unused_dataset(mocker: MockerFixture):
    dataframe = DataFrame({
        TransactionInferences.is_fraud.key: [1.0],
        TransactionInferences.transaction_timestamp.key: [datetime.now()],
    })
    mocker.patch.object(dataframe, "__len__", return_value=DatasetConfig.minimum_rows)
    mocker.patch(
        target="services.train_model.src.repositories.postgres.transaction_inferences.pandas.read_sql",
        return_value=dataframe
    )

    result = get_timed_latest_unused_dataset()

    pandas.testing.assert_frame_equal(result.dataset, dataframe)