from slack_bolt import Ack
from slack_sdk import WebClient

from fraud_detection_api.services.slack import slack_app
from fraud_detection_api.modules.schemas.slack import TrainingValue
from fraud_detection_api.services.mwaa import trigger_airflow_dag
from fraud_detection_api.services.idempotency import slack_action_store
from fraud_detection_api.services.slack import update_message

@slack_app.state("approve_training")
def approve_training(
    ack: Ack,
    body: dict,
    action: dict,
    client: WebClient
):
    ack()
    with slack_action_store.guard(action["action_id"], body["message"]["ts"]):
        training_value = TrainingValue.model_validate_json(action["value"])
        trigger_airflow_dag(
            dag_id="on_training_decision",
            configurations={
                "approved": True,
                "model_deployment_workflow": {
                    "id": str(training_value.workflow_id),
                },
                "should_train_for_promotion": training_value.should_train_for_promotion
            }
        )
        update_message(
            client=client,
            body=body,
            text_markdown=f"✅ *Training approved* by @{body['user']['username']}, added to queue..."
        )

@slack_app.state("reject_training")
def reject_training(
    ack: Ack,
    body: dict,
    action: dict,
    client: WebClient
):
    ack()
    with slack_action_store.guard(action["action_id"], body["message"]["ts"]):
        training_value = TrainingValue.model_validate_json(action["value"])
        trigger_airflow_dag(
            dag_id="on_training_decision",
            configurations={
                "approved": False,
                "model_deployment_workflow": {
                    "id": str(training_value.workflow_id),
                },
                "should_train_for_promotion": training_value.should_train_for_promotion
            }
        )
        update_message(
            client=client,
            body=body,
            text_markdown=f"❌ *Training dismissed* by @{body['user']['username']}."
        )