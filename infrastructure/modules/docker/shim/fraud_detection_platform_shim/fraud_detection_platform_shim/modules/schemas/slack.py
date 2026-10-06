from uuid import UUID

from pydantic import BaseModel, StrictBool, ConfigDict, StrictStr

class TrainingValue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: UUID
    should_train_for_promotion: StrictBool

    mwaa_environment_name: StrictStr
    aws_endpoint_url_mwaa: StrictStr

class PromotionValue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: UUID

    mwaa_environment_name: StrictStr
    aws_endpoint_url_mwaa: StrictStr