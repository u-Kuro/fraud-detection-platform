from datetime import datetime, timezone, timedelta
from typing import cast
from uuid import uuid4

from pandas import DataFrame

from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences
from seed_transaction_inferences.repositories.postgres.postgres import sql_session
from seed_transaction_inferences.repositories.postgres.transaction_inferences import bulk_insert_transaction_inferences
from seed_transaction_inferences.repositories.s3.transaction_inferences_seed import get_transaction_inferences_seed_csv

def transform_transaction_inferences_seed_csv(dataframe: DataFrame) -> list[dict[str, object]]:
    records = []
    epoch = datetime(2013, 9, 1, tzinfo=timezone.utc)

    for row in dataframe.itertuples(index=False):
        is_fraud = bool(cast(int, row.Class))
        records.append({
            TransactionInferences.transaction_id.key: uuid4(),
            TransactionInferences.transaction_timestamp.key: epoch + timedelta(seconds=cast(float, row.Time)),
            TransactionInferences.amount.key: cast(float, row.Amount),
            TransactionInferences.is_fraud.key: is_fraud,
            TransactionInferences.is_fraud_prediction.key: is_fraud,
            TransactionInferences.is_fraud_probability.key: float(is_fraud),
            **{
                f"v{i}": cast(float, getattr(row, f"V{i}"))
                for i in range(1, 29)
            },
        })
    return records

def seed_transaction_inferences() -> None:
    dataframe = get_transaction_inferences_seed_csv()
    records = transform_transaction_inferences_seed_csv(dataframe)

    with sql_session.begin() as session:
        bulk_insert_transaction_inferences(session, records)