from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class AirflowConfig:
    @classmethod
    @validated_lru_cache
    def MWAA_ENVIRONMENT_NAME(cls) -> StrictStr:
        return Variable.get(cls.MWAA_ENVIRONMENT_NAME.__name__)

    @classmethod
    @validated_lru_cache
    def AWS_ENDPOINT_URL_MWAA(cls) -> StrictStr:
        return Variable.get(cls.AWS_ENDPOINT_URL_MWAA.__name__)