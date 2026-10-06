import uuid
from datetime import datetime

from sqlalchemy import UUID, func, DateTime, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from dags.shared.modules.schemas.postgres.postgres import PostgresTableBase

class TransactionInferences(PostgresTableBase):
    __tablename__ = "transaction_inferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    transaction_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    is_fraud: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_fraud_prediction: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_fraud_probability: Mapped[float] = mapped_column(Float, nullable=False)
    model_deployment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=False)
    v1: Mapped[float] = mapped_column(Float, nullable=False)
    v2: Mapped[float] = mapped_column(Float, nullable=False)
    v3: Mapped[float] = mapped_column(Float, nullable=False)
    v4: Mapped[float] = mapped_column(Float, nullable=False)
    v5: Mapped[float] = mapped_column(Float, nullable=False)
    v6: Mapped[float] = mapped_column(Float, nullable=False)
    v7: Mapped[float] = mapped_column(Float, nullable=False)
    v8: Mapped[float] = mapped_column(Float, nullable=False)
    v9: Mapped[float] = mapped_column(Float, nullable=False)
    v10: Mapped[float] = mapped_column(Float, nullable=False)
    v11: Mapped[float] = mapped_column(Float, nullable=False)
    v12: Mapped[float] = mapped_column(Float, nullable=False)
    v13: Mapped[float] = mapped_column(Float, nullable=False)
    v14: Mapped[float] = mapped_column(Float, nullable=False)
    v15: Mapped[float] = mapped_column(Float, nullable=False)
    v16: Mapped[float] = mapped_column(Float, nullable=False)
    v17: Mapped[float] = mapped_column(Float, nullable=False)
    v18: Mapped[float] = mapped_column(Float, nullable=False)
    v19: Mapped[float] = mapped_column(Float, nullable=False)
    v20: Mapped[float] = mapped_column(Float, nullable=False)
    v21: Mapped[float] = mapped_column(Float, nullable=False)
    v22: Mapped[float] = mapped_column(Float, nullable=False)
    v23: Mapped[float] = mapped_column(Float, nullable=False)
    v24: Mapped[float] = mapped_column(Float, nullable=False)
    v25: Mapped[float] = mapped_column(Float, nullable=False)
    v26: Mapped[float] = mapped_column(Float, nullable=False)
    v27: Mapped[float] = mapped_column(Float, nullable=False)
    v28: Mapped[float] = mapped_column(Float, nullable=False)