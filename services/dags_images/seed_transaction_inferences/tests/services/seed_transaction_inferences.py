from datetime import datetime, timezone
from uuid import UUID

import pandas

from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences
from seed_transaction_inferences.services.seed_transaction_inferences import transform_transaction_inferences_seed_csv

def test_transform_transaction_inferences_seed_csv():
    dataframe = pandas.DataFrame({
        "Time": [0],
        "Amount": [1.0],
        "Class": [0],
        **{f"V{i}": [1.0] for i in range(1, 29)},
    })

    row = transform_transaction_inferences_seed_csv(dataframe=dataframe)[0]

    assert isinstance(row[TransactionInferences.transaction_id.key], UUID)

    transaction_timestamp = row[TransactionInferences.transaction_timestamp.key]
    assert isinstance(transaction_timestamp, datetime)
    assert transaction_timestamp.tzinfo is timezone.utc

    amount = row[TransactionInferences.amount.key]
    assert isinstance(amount, float)
    assert amount == 1.0

    assert row[TransactionInferences.is_fraud.key] is False
    assert row[TransactionInferences.is_fraud_prediction.key] is False

    is_fraud_probability = row[TransactionInferences.is_fraud_probability.key]
    assert isinstance(is_fraud_probability, float)
    assert is_fraud_probability == 0.0

    assert all(
        type(row[f"v{i}"]) is float and row[f"v{i}"] == 1.0
        for i in range(1, 29)
    )