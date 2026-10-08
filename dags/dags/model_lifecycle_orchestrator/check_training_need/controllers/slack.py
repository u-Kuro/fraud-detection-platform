import json
from uuid import UUID

from airflow.sdk import task

from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.tasks import ExpiredAndReservedModelDeploymentWorkflows, ModelDeploymentWorkflowForTraining
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.xcom import DriftCheckResult
from dags.shared.modules.configs.airflow.airflow import AirflowConfig
from dags.shared.modules.configs.slack import SlackConfig
from dags.shared.services.slack import create_blocks, slack_client

@task
def invalidate_expired_promotion_approval(data: ExpiredAndReservedModelDeploymentWorkflows | None):
    assert data is not None

    slack_client.chat_update(
        ts=data.expired.slack_promotion_approval_message_ts,
        channel=SlackConfig.SLACK_CHANNEL_ID(),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"~{(
                        "⚠️ Challenger Model Promotion Required"
                    )}~"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "🔄 Expired: a newer request will be issued."
                    }
                ]
            }
        ]
    )

@task
def invalidate_old_training_approval(
    model_deployment_workflow_for_training: ModelDeploymentWorkflowForTraining | None,
    drift_result: DriftCheckResult | None,
):
    assert model_deployment_workflow_for_training is not None

    if model_deployment_workflow_for_training.slack_training_approval_message_ts is None: return

    slack_client.chat_update(
        ts=model_deployment_workflow_for_training.slack_training_approval_message_ts,
        channel=SlackConfig.SLACK_CHANNEL_ID(),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"~{(
                        "🆕 First Training Required"
                        if drift_result is None
                        else "⚠️ Model Retraining Required"
                    )}~"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "🔄 Expired: a newer request will be issued."
                    }
                ]
            }
        ]
    )

def build_training_approval_blocks_initializing(
    drift_result: DriftCheckResult | None
) -> list:
    if drift_result is None:
        return create_blocks(
            title="🆕 First Training Required",
            body=(
                "No model has been deployed yet. "
                "Please wait, this approval request is initializing..."
            ),
        )
    else:
        drift_summary = drift_result.drift_summary
        data_drift = drift_summary["data_drift"]
        concept_drift = drift_summary["concept_drift"]

        features_drift_text = (
            f"`{data_drift.get('number_of_drifted_features', 0)} / "
            f"{data_drift.get('number_of_features', 0)} features "
            f"({data_drift.get('share_of_drifted_features', 0.0):.2%})`"
        )

        if concept_drift.get("skipped", False):
            concept_drift_text = "`Not evaluated, fewer than 100 fraud samples`"
        else:
            f1 = concept_drift["f1"]
            f1_delta = concept_drift["f1_delta"]
            precision = concept_drift["precision"]
            precision_delta = concept_drift["precision_delta"]
            recall = concept_drift["recall"]
            recall_delta = concept_drift["recall_delta"]

            concept_drift_text = (
                f"  • F1: `{f1:.2%} ({f1_delta * 100:+.2f} pp)`\n"
                f"  • Recall: `{recall:.2%} ({recall_delta * 100:+.2f} pp)`\n"
                f"  • Precision: `{precision:.2%} ({precision_delta * 100:+.2f} pp)`"
            )

        return create_blocks(
            title="⚠️ Model Retraining Required",
            body=(
                "Significant data or concept drift has been detected in production.\n\n"
    
                f"*Features drifted:* {features_drift_text}\n"
                f"*Concept drifted:* \n{concept_drift_text}\n\n"
    
                "Please wait, this approval request is initializing..."
            ),
        )

@task
def initialize_training_approval(
    model_deployment_workflow_for_training: ModelDeploymentWorkflowForTraining | None,
    drift_result: DriftCheckResult | None,
) -> ModelDeploymentWorkflowForTraining:
    assert model_deployment_workflow_for_training is not None

    response = slack_client.chat_postMessage(
        channel=SlackConfig.SLACK_CHANNEL_ID(),
        blocks=build_training_approval_blocks_initializing(
            drift_result=drift_result
        )
    )
    slack_training_approval_message_ts = response["ts"]

    assert isinstance(slack_training_approval_message_ts, str)

    model_deployment_workflow_for_training.slack_training_approval_message_ts = slack_training_approval_message_ts

    return model_deployment_workflow_for_training

def training_decision_buttons(
    workflow_id: UUID,
    should_train_for_promotion: bool
) -> list[dict]:
    return [
        {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "✅ Approve Training"
            },
            "style": "primary",
            "action_id": "training_decision:approved",
            "value": json.dumps({
                "approved": True,
                "workflow_id": str(workflow_id),
                "should_train_for_promotion": should_train_for_promotion,
                "mwaa_environment_name": AirflowConfig.MWAA_ENVIRONMENT_NAME(),
                "aws_endpoint_url_mwaa": AirflowConfig.AWS_ENDPOINT_URL_MWAA(),
            })
        },
        {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "❌ Dismiss"
            },
            "style": "danger",
            "action_id": "training_decision:rejected",
            "value": json.dumps({
                "approved": False,
                "workflow_id": str(workflow_id),
                "should_train_for_promotion": should_train_for_promotion,
                "mwaa_environment_name": AirflowConfig.MWAA_ENVIRONMENT_NAME(),
                "aws_endpoint_url_mwaa": AirflowConfig.AWS_ENDPOINT_URL_MWAA(),
            })
        },
    ]

def build_training_approval_blocks(
    workflow_id: UUID,
    drift_result: DriftCheckResult | None,
    should_train_for_promotion: bool,
) -> list[dict]:
    if drift_result is None:
        return create_blocks(
            title="🆕 First Training Required",
            body=(
                "No model has been deployed yet. "
                "Click *Approve Training* to train a model."
            ),
            buttons=training_decision_buttons(
                workflow_id=workflow_id,
                should_train_for_promotion=should_train_for_promotion
            )
        )
    else:
        drift_summary = drift_result.drift_summary
        data_drift = drift_summary["data_drift"]
        concept_drift = drift_summary["concept_drift"]

        features_drift_text = (
            f"`{data_drift.get('number_of_drifted_features', 0)} of "
            f"{data_drift.get('number_of_features', 0)} features "
            f"({data_drift.get('share_of_drifted_features', 0.0):.2%})`"
        )

        if concept_drift.get("skipped", False):
            concept_drift_text = "`Not evaluated, fewer than 100 fraud samples`"
        else:
            f1 = concept_drift["f1"]
            f1_delta = concept_drift["f1_delta"]
            precision = concept_drift["precision"]
            precision_delta = concept_drift["precision_delta"]
            recall = concept_drift["recall"]
            recall_delta = concept_drift["recall_delta"]

            concept_drift_text = (
                f"  • F1: `{f1:.2%} ({f1_delta * 100:+.2f} pp)`\n"
                f"  • Recall: `{recall:.2%} ({recall_delta * 100:+.2f} pp)`\n"
                f"  • Precision: `{precision:.2%} ({precision_delta * 100:+.2f} pp)`"
            )

        return create_blocks(
            title="⚠️ Model Retraining Required",
            body=(
                "Significant data or concept drift has been detected in production.\n\n"

                f"*Features drifted:* {features_drift_text}\n"
                f"*Concept drifted:* \n{concept_drift_text}\n\n"

                "Click *Approve Training* to kick off a new training run."
            ),
            buttons=training_decision_buttons(
                workflow_id=workflow_id,
                should_train_for_promotion=should_train_for_promotion
            )
        )

@task
def update_training_approval(
    model_deployment_workflow_for_training: ModelDeploymentWorkflowForTraining,
    drift_result: DriftCheckResult | None,
):
    assert model_deployment_workflow_for_training.slack_training_approval_message_ts is not None
    assert model_deployment_workflow_for_training.id is not None

    slack_client.chat_update(
        ts=model_deployment_workflow_for_training.slack_training_approval_message_ts,
        channel=SlackConfig.SLACK_CHANNEL_ID(),
        blocks=build_training_approval_blocks(
            workflow_id=model_deployment_workflow_for_training.id,
            drift_result=drift_result,
            should_train_for_promotion=model_deployment_workflow_for_training.should_train_for_promotion
        )
    )