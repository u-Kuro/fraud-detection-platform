from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, StrictBool, Strict

class ModelDeploymentWorkflowForPromotion(BaseModel):
    id: UUID

class PromotionDecision(BaseModel):
    approved: StrictBool
    model_deployment_workflow: ModelDeploymentWorkflowForPromotion

class PromotedModelDeployment(BaseModel):
    dataset_max_timestamp: Annotated[datetime, Strict()]