from numpy import ndarray
from pydantic import BaseModel, ConfigDict, StrictFloat
from sklearn.model_selection import StratifiedKFold

class PreprocessOutputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    x_train: ndarray
    x_test: ndarray
    y_train: ndarray
    y_test: ndarray
    cross_validation: StratifiedKFold