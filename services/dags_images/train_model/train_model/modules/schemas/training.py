from typing import Any, Annotated

from imblearn.pipeline import Pipeline
from pydantic import BaseModel, ConfigDict, StrictStr, Strict

class TrainModelOutputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Pipeline
    hyperparameters: Annotated[dict[StrictStr, Any], Strict()]