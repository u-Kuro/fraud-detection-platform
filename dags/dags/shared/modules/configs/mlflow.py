from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class MLflowConfig:
    challenger_alias: str = "challenger"

    @classmethod
    @validate_call(validate_return=True)
    def MLFLOW_TRACKING_URI(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_TRACKING_URI.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def MLFLOW_TRACKING_USERNAME(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_TRACKING_USERNAME.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def MLFLOW_TRACKING_PASSWORD(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_TRACKING_PASSWORD.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def MLFLOW_WORKSPACE(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_WORKSPACE.__name__)
