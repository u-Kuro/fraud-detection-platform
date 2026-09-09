from pydantic import StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from dags.shared.modules.configs.airflow.airflow import AirflowConfig

class ECREnvironment(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=AirflowConfig.environment_prefix,
        case_sensitive=True
    )

    DRIFT_CHECK_IMAGE: StrictStr
    TRAIN_MODEL_IMAGE: StrictStr
    ARCHIVE_IMAGE: StrictStr

ecr_environment = ECREnvironment()