from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class ECRConfig:
    @classmethod
    @validated_lru_cache
    def archive_image(cls) -> StrictStr:
        return Variable.get(cls.archive_image.__name__)

    @classmethod
    @validated_lru_cache
    def drift_check_image(cls) -> StrictStr:
        return Variable.get(cls.drift_check_image.__name__)

    @classmethod
    @validated_lru_cache
    def train_model_image(cls) -> StrictStr:
        return Variable.get(cls.train_model_image.__name__)