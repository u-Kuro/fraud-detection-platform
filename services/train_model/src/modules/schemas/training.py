from typing import Any, Annotated

from pydantic import BaseModel, ConfigDict, StrictStr, Strict
from sklearn.pipeline import Pipeline

class TrainModelOutputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Annotated[Pipeline, Strict()]
    hyperparameters: Annotated[dict[StrictStr, Any], Strict()]