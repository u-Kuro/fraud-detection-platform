from dataclasses import dataclass

from services.fraud_detection_api.src.modules.schemas.mlflow import DeployedModel
from services.fraud_detection_api.src.repositories.postgres.model_deployments import get_active_model_deployment

@dataclass(frozen=True)
class FraudClassifierConfig:
    classification_threshold: float = 0.5
    deployed_model: DeployedModel = get_active_model_deployment()