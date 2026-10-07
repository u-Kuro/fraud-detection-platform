from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class AirflowConfig:
    @classmethod
    @validate_call(validate_return=True)
    def MWAA_ENVIRONMENT_NAME(cls) -> StrictStr:
        return Variable.get(cls.MWAA_ENVIRONMENT_NAME.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def AWS_ENDPOINT_URL_MWAA(cls) -> StrictStr:
        return Variable.get(cls.AWS_ENDPOINT_URL_MWAA.__name__)