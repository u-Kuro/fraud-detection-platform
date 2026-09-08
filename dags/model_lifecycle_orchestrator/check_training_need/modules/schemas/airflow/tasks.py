from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StrictStr, StrictInt, StrictBool, Strict

class ExpiredModelDeploymentWorkflow(BaseModel):
    id: Annotated[UUID, Strict()]
    model_name: StrictStr
    model_version: StrictInt
    mlflow_run_id: StrictStr
    slack_promotion_approval_message_ts: StrictStr

class ReservedModelDeploymentWorkflow(BaseModel):
    model_name: StrictStr
    model_version: StrictInt

class ExpiredAndReservedModelDeploymentWorkflows(BaseModel):
    expired: ExpiredModelDeploymentWorkflow
    reserved: ReservedModelDeploymentWorkflow

class ActiveModelDeployment(BaseModel):
    mlflow_run_id: StrictStr

class ModelDeploymentWorkflowForTraining(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    state: StrictStr
    should_train_for_promotion: StrictBool
    id: Annotated[UUID, Strict()] | None = None
    slack_training_approval_message_ts: StrictStr | None = None