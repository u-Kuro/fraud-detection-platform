from datetime import datetime
from uuid import UUID

from airflow.sdk.serde import allow_class
from pydantic import BaseModel, StrictBool

class ModelDeploymentWorkflowForPromotion(BaseModel):
    id: UUID

class PromotionDecision(BaseModel):
    approved: StrictBool
    model_deployment_workflow: ModelDeploymentWorkflowForPromotion

class PromotedModelDeployment(BaseModel):
    dataset_max_timestamp: datetime

allow_class(PromotionDecision)