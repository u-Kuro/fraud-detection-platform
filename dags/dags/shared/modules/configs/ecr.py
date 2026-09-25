from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class ECRConfig:
    @classmethod
    @validated_lru_cache
    def ARCHIVE_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.ARCHIVE_IMAGE.__name__)

    @classmethod
    @validated_lru_cache
    def DRIFT_CHECK_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.DRIFT_CHECK_IMAGE.__name__)

    @classmethod
    @validated_lru_cache
    def TRAIN_MODEL_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.TRAIN_MODEL_IMAGE.__name__)