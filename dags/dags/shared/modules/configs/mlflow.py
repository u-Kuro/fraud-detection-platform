from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class MLflowConfig:
    challenger_alias: str = "challenger"

    @classmethod
    @validated_lru_cache
    def mlflow_tracking_uri(cls) -> StrictStr:
        return Variable.get(cls.mlflow_tracking_uri.__name__)

    @classmethod
    @validated_lru_cache
    def mlflow_tracking_username(cls) -> StrictStr:
        return Variable.get(cls.mlflow_tracking_username.__name__)

    @classmethod
    @validated_lru_cache
    def mlflow_tracking_password(cls) -> StrictStr:
        return Variable.get(cls.mlflow_tracking_password.__name__)

    @classmethod
    @validated_lru_cache
    def mlflow_workspace(cls) -> StrictStr:
        return Variable.get(cls.mlflow_workspace.__name__)
