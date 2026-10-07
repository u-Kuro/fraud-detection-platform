from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class S3Config:
    @classmethod
    @validate_call(validate_return=True)
    def S3_BUCKET(cls) -> StrictStr:
        return Variable.get(cls.S3_BUCKET.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def S3_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.S3_CONNECTION_ID.__name__)