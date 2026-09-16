from typing import Any, Annotated

from pydantic import BaseModel, ConfigDict, StrictStr, Strict
from sklearn.pipeline import Pipeline

class TrainModelOutputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Pipeline
    hyperparameters: Annotated[dict[StrictStr, Any], Strict()]