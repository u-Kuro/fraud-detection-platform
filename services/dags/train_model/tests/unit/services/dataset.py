import copy
from datetime import datetime, timedelta, timezone

from pandas import DataFrame

from services.shared.src.modules.schemas.postgres.transaction_inferences import TransactionInferences
from services.dags.train_model.src.services.dataset import get_dataset_min_and_max_timestamps

def test_get_dataset_min_and_max_timestamps():
    today = datetime.now(tz=timezone.utc)
    yesterday = today - timedelta(days=1)

    original_today = copy.deepcopy(today)
    original_yesterday = copy.deepcopy(yesterday)

    timestamp_feature_key = TransactionInferences.transaction_timestamp.key
    dataframe = DataFrame({
        timestamp_feature_key: [
            yesterday,
            today,
        ],
    })
    dataframe[timestamp_feature_key] = dataframe[timestamp_feature_key].astype("datetime64[s, UTC]").astype("int64")

    result = get_dataset_min_and_max_timestamps(
        dataset=dataframe,
        timestamp_feature_key=timestamp_feature_key
    )

    assert result.model_dataset_min_iso_datetime == original_yesterday.replace(microsecond=0).isoformat()
    assert result.model_dataset_max_iso_datetime == original_today.replace(microsecond=0).isoformat()