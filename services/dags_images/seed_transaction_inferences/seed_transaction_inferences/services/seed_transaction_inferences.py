from datetime import datetime, timezone, timedelta
from uuid import uuid4

from pandas import DataFrame

from seed_transaction_inferences.repositories.postgres.transaction_inferences import bulk_insert_transaction_inferences
from seed_transaction_inferences.repositories.s3.transaction_inferences_seed import get_transaction_inferences_seed_iterator
from seed_transaction_inferences.repositories.postgres.postgres import sql_session
from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences

def transform_transaction_inferences_seed(dataframe: DataFrame) -> list[dict[str, object]]:
    start_date = datetime(2013, 9, 1, tzinfo=timezone.utc)
    pca_feature_keys = [f"v{i}" for i in range(1, 29)]

    records = []
    ordered_column_dataframe_iterator = dataframe[["Time", "Amount", "Class", *[f"V{i}" for i in range(1, 29)]]].itertuples(index=False, name=None)

    for seconds_duration, amount, fraud_class, *pca_features in ordered_column_dataframe_iterator:
        is_fraud = bool(fraud_class)
        records.append({
            TransactionInferences.transaction_id.key: uuid4(),
            TransactionInferences.transaction_timestamp.key: start_date + timedelta(seconds=float(seconds_duration)),
            TransactionInferences.amount.key: float(amount),
            TransactionInferences.is_fraud.key: is_fraud,
            TransactionInferences.is_fraud_prediction.key: is_fraud,
            TransactionInferences.is_fraud_probability.key: float(is_fraud),
            **{
                key: float(value)
                for key, value in zip(pca_feature_keys, pca_features, strict=True)
            },
        })
    return records

def seed_transaction_inferences() -> None:
    with sql_session.begin() as session:
        for dataframe in get_transaction_inferences_seed_iterator():
            bulk_insert_transaction_inferences(
                session,
                transform_transaction_inferences_seed(dataframe),
            )