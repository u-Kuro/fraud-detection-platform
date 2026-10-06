from slack_bolt import Ack
from slack_sdk import WebClient

from fraud_detection_platform_shim.services.slack import slack_app
from fraud_detection_platform_shim.modules.schemas.slack import PromotionValue
from fraud_detection_platform_shim.services.mwaa import trigger_airflow_dag
from fraud_detection_platform_shim.services.idempotency import slack_action_store
from fraud_detection_platform_shim.services.slack import update_message

@slack_app.action("approve_promotion")
def approve_promotion(
    ack: Ack,
    body: dict,
    action: dict,
    client: WebClient
):
    ack()
    with slack_action_store.guard(action["action_id"], body["message"]["ts"]):
        promotion_value = PromotionValue.model_validate_json(action["value"])
        trigger_airflow_dag(
            dag_id="on_promotion_decision",
            endpoint_url=promotion_value.aws_endpoint_url_mwaa,
            environment_name=promotion_value.mwaa_environment_name,
            configurations={
                "approved": True,
                "model_deployment_workflow": {
                    "id": str(promotion_value.workflow_id),
                }
            }
        )
        update_message(
            client=client,
            body=body,
            text_markdown=f"🚀 *Promotion approved* by @{body['user']['username']}, added to queue..."
        )

@slack_app.action("reject_promotion")
def reject_promotion(
    ack: Ack,
    body: dict,
    action: dict,
    client: WebClient
):
    ack()
    with slack_action_store.guard(action["action_id"], body["message"]["ts"]):
        promotion_value = PromotionValue.model_validate_json(action["value"])
        trigger_airflow_dag(
            dag_id="on_promotion_decision",
            endpoint_url=promotion_value.aws_endpoint_url_mwaa,
            environment_name=promotion_value.mwaa_environment_name,
            configurations={
                "approved": False,
                "model_deployment_workflow": {
                    "id": str(promotion_value.workflow_id),
                }
             }
        )
        update_message(
            client=client,
            body=body,
            text_markdown=f"❌ *Promotion dismissed* by @{body['user']['username']}."
        )