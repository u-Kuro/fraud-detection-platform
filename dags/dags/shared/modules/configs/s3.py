from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class S3Config:
    @classmethod
    @validated_lru_cache
    def S3_BUCKET(cls) -> StrictStr:
        return Variable.get(cls.S3_BUCKET.__name__)

    @classmethod
    @validated_lru_cache
    def S3_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.S3_CONNECTION_ID.__name__)