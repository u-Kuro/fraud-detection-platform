import uuid
from datetime import datetime

from sqlalchemy import UUID, func, DateTime, Text, Integer, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column

from dags.shared.modules.schemas.postgres.postgres import PostgresTableBase

class ModelDeployments(PostgresTableBase):
    __tablename__ = "model_deployments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    mlflow_run_id: Mapped[str] = mapped_column(Text, nullable=False)
    dataset_min_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dataset_max_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())