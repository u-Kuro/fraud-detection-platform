from datetime import datetime, timedelta, timezone

from pandas import DataFrame

from services.shared.src.modules.schemas.postgres.transaction_inferences import TransactionInferences
from services.train_model.src.services.dataset import get_dataset_min_and_max_timestamps

def test_get_dataset_min_and_max_timestamps():
    timestamp_feature_key = TransactionInferences.transaction_timestamp.key
    today = datetime.now()
    yesterday = datetime.now() - timedelta(days=1)
    dataframe = DataFrame({
        timestamp_feature_key: [
            yesterday,
            today,
        ],
    })

    result = get_dataset_min_and_max_timestamps(
        dataset=dataframe,
        timestamp_feature_key=timestamp_feature_key
    )

    assert result.model_dataset_min_iso_datetime == yesterday.astimezone(timezone.utc).isoformat()
    assert result.model_dataset_max_iso_datetime == today.astimezone(timezone.utc).isoformat()