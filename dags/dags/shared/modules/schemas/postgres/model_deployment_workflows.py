import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import UUID, func, DateTime, Enum, Boolean, false, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from dags.shared.modules.schemas.postgres.postgres import PostgresTableBase

class ModelDeploymentWorkflowState(StrEnum):
    train_pending = "train_pending"
    promote_pending = "promote_pending"
    reserved = "reserved"

class ModelDeploymentWorkflows(PostgresTableBase):
    __tablename__ = "model_deployment_workflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    state: Mapped[ModelDeploymentWorkflowState] = mapped_column(
        Enum(
            ModelDeploymentWorkflowState,
            native_enum=False,
            create_constraint=True,
            name="state_check",
        ),
        nullable=False
    )
    training_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    promotion_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    model_trained_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    mlflow_run_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    registered_model_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    registered_model_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    model_dataset_min_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    model_dataset_max_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    slack_training_approval_message_ts: Mapped[str | None] = mapped_column(Text, nullable=True)
    slack_promotion_approval_message_ts: Mapped[str | None] = mapped_column(Text, nullable=True)