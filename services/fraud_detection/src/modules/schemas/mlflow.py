from pydantic import BaseModel, StrictStr, StrictInt, ConfigDict

class DeployedModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    model_name: StrictStr
    model_version: StrictInt