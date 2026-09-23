from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class S3Config:
    @classmethod
    @validated_lru_cache
    def s3_bucket(cls) -> StrictStr:
        return Variable.get(cls.s3_bucket.__name__)

    @classmethod
    @validated_lru_cache
    def s3_connection_id(cls) -> StrictStr:
        return Variable.get(cls.s3_connection_id.__name__)