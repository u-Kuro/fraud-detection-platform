from sqlalchemy import insert
from sqlalchemy.orm import Session

from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences

def bulk_insert_transaction_inferences(
    session: Session,
    records: list[dict],
) -> None:
    session.execute(
        insert(TransactionInferences),
        records,
    )