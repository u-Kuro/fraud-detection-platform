import re

from slack_bolt import Ack
from slack_sdk import WebClient

from fraud_detection_platform_shim.services.slack import slack_app
from fraud_detection_platform_shim.modules.schemas.slack import TrainingValue
from fraud_detection_platform_shim.services.mwaa import trigger_airflow_dag
from fraud_detection_platform_shim.services.idempotency import slack_action_store
from fraud_detection_platform_shim.services.slack import update_message

@slack_app.action(re.compile(r"^training_decision:"))
def training_decision(
    ack: Ack,
    body: dict,
    action: dict,
    client: WebClient
):
    ack()
    with slack_action_store.guard(training_decision.__name__, body["message"]["ts"]):
        training_value = TrainingValue.model_validate_json(action["value"])
        trigger_airflow_dag(
            dag_id="on_training_decision",
            endpoint_url=training_value.aws_endpoint_url_mwaa,
            environment_name=training_value.mwaa_environment_name,
            configurations={
                "approved": training_value.approved,
                "model_deployment_workflow": {
                    "id": str(training_value.workflow_id),
                },
                "should_train_for_promotion": training_value.should_train_for_promotion
            }
        )

        username = body["user"]["username"]
        update_message(
            client=client,
            body=body,
            text_markdown=(
                f"✅ *Training approved* by @{username}, added to queue..."
                if training_value.approved else
                f"❌ *Training dismissed* by @{username}."
            )
        )