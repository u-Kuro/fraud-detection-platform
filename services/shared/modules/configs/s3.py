from dataclasses import dataclass

from shared.modules.configs.mlflow import MLflowConfig
from shared.modules.configs.project import ProjectConfig
from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences

@dataclass(frozen=True)
class S3Config:
    model_drift_path: str = f"{ProjectConfig.project_name}/monitoring/drift/{MLflowConfig.model_name}"
    transaction_inferences_archive_path: str = f"{ProjectConfig.project_name}/data/archive/{TransactionInferences.__tablename__}"