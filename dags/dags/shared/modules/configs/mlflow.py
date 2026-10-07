from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class MLflowConfig:
    challenger_alias: str = "challenger"

    @classmethod
    @validated_lru_cache
    def MLFLOW_TRACKING_URI(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_TRACKING_URI.__name__)

    @classmethod
    @validated_lru_cache
    def MLFLOW_TRACKING_USERNAME(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_TRACKING_USERNAME.__name__)

    @classmethod
    @validated_lru_cache
    def MLFLOW_TRACKING_PASSWORD(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_TRACKING_PASSWORD.__name__)

    @classmethod
    @validated_lru_cache
    def MLFLOW_WORKSPACE(cls) -> StrictStr:
        return Variable.get(cls.MLFLOW_WORKSPACE.__name__)
