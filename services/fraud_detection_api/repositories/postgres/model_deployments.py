from sqlalchemy import select

from fraud_detection_api.modules.schemas.mlflow import DeployedModel
from fraud_detection_api.repositories.postgres.postgres import sql_session
from shared.modules.configs.postgres import PostgresConfig
from shared.modules.schemas.postgres.model_deployments import ModelDeployments

def get_active_model_deployment() -> DeployedModel:
    with sql_session.begin() as session:
        (name, version) = session.execute(
            select(
                ModelDeployments.name,
                ModelDeployments.version
            )
            .where(
                ModelDeployments.project_id == PostgresConfig.project_id,
                ModelDeployments.active.is_(True),
            )
            .limit(1)
        ).one().t

    return DeployedModel(
        model_name=name,
        model_version=version
    )