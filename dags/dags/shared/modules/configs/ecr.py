from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class ECRConfig:
    @classmethod
    @validate_call(validate_return=True)
    def ARCHIVE_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.ARCHIVE_IMAGE.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def DRIFT_CHECK_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.DRIFT_CHECK_IMAGE.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def SEED_TRANSACTION_INFERENCES_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.SEED_TRANSACTION_INFERENCES_IMAGE.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def TRAIN_MODEL_IMAGE(cls) -> StrictStr:
        return Variable.get(cls.TRAIN_MODEL_IMAGE.__name__)