from unittest.mock import patch
from uuid import uuid4

from fraud_detection_api.modules.schemas.mlflow import DeployedModel

# MLflow
patch(target="mlflow.set_experiment").start()
patch(target="mlflow.pyfunc.load_model").start()
patch(target="mlflow.log_artifact").start()
patch(target="mlflow.log_figure").start()

# Postgres
patch(
    target="shared.repositories.postgres.projects.get_project_id",
    return_value=uuid4()
).start()
patch(
    target="fraud_detection_api.repositories.postgres.model_deployments.get_active_model_deployment",
    return_value=DeployedModel(
        model_name="model",
        model_version=1
    )
).start()

# S3
patch(target="boto3.s3.inject.upload_fileobj").start()
patch(target="slack_bolt.App").start()
