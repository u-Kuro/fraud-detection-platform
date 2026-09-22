from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StrictStr, Strict

from dags_shared.modules.schemas.postgres.model_deployment_workflows import ModelDeploymentWorkflowState

class ModelDeploymentWorkflow(BaseModel):
    id: Annotated[UUID, Strict()]
    state: Annotated[ModelDeploymentWorkflowState, Strict()]
    slack_training_approval_message_ts: StrictStr