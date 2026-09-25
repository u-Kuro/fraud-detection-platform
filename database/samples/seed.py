import csv
import gzip
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models import TransactionInference

def seed_transactions(
    session: Session,
    file_path: str,
    batch_size: int = 5_000,
) -> None:
    if session.query(TransactionInference).first() is not None:
        return

    batch = []

    with gzip.open(file_path, "rt", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            batch.append(
                {
                    "transaction_id": uuid4(),
                    "transaction_timestamp": (
                        datetime(2019, 1, 1, tzinfo=timezone.utc)
                        + timedelta(seconds=float(row["Time"]))
                    ),
                    "v1": float(row["V1"]),
                    "v2": float(row["V2"]),
                    "v3": float(row["V3"]),
                    "v4": float(row["V4"]),
                    "v5": float(row["V5"]),
                    "v6": float(row["V6"]),
                    "v7": float(row["V7"]),
                    "v8": float(row["V8"]),
                    "v9": float(row["V9"]),
                    "v10": float(row["V10"]),
                    "v11": float(row["V11"]),
                    "v12": float(row["V12"]),
                    "v13": float(row["V13"]),
                    "v14": float(row["V14"]),
                    "v15": float(row["V15"]),
                    "v16": float(row["V16"]),
                    "v17": float(row["V17"]),
                    "v18": float(row["V18"]),
                    "v19": float(row["V19"]),
                    "v20": float(row["V20"]),
                    "v21": float(row["V21"]),
                    "v22": float(row["V22"]),
                    "v23": float(row["V23"]),
                    "v24": float(row["V24"]),
                    "v25": float(row["V25"]),
                    "v26": float(row["V26"]),
                    "v27": float(row["V27"]),
                    "v28": float(row["V28"]),
                    "amount": float(row["Amount"]),
                    "is_fraud": row["Class"].lower() == "true",
                }
            )

            if len(batch) >= batch_size:
                session.execute(insert(TransactionInference), batch)
                session.commit()
                batch.clear()

        if batch:
            session.execute(insert(TransactionInference), batch)
            session.commit()