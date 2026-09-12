from unittest.mock import patch

from services.fraud_detection_api.src.modules.schemas.mlflow import DeployedModel

# noinspection unused-imports
import services.shared.tests.conftest  # noqa: F401

# Postgres
patch(
    target="services.fraud_detection_api.src.repositories.postgres.model_deployments.get_active_model_deployment",
    return_value=DeployedModel(
        model_name="model",
        model_version=1
    )
).start()

# Slack
patch(target="slack_bolt.App").start()
