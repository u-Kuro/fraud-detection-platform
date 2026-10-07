from uuid import UUID

from airflow.sdk.serde import allow_class
from pydantic import BaseModel, StrictStr

from dags.shared.modules.schemas.postgres.model_deployment_workflows import ModelDeploymentWorkflowState

class ModelDeploymentWorkflow(BaseModel):
    id: UUID
    state: ModelDeploymentWorkflowState
    slack_training_approval_message_ts: StrictStr | None

allow_class(ModelDeploymentWorkflow)