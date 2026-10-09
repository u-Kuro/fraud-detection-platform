import json
from uuid import uuid4, UUID

from pytest_mock import MockerFixture

from dags.model_lifecycle_orchestrator.check_training_need.controllers.slack import build_training_approval_blocks_initializing, initialize_training_approval, training_decision_buttons, build_training_approval_blocks
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.tasks import ModelDeploymentWorkflowForTraining
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.xcom import DriftCheckResult
from dags.shared.modules.configs.airflow.airflow import AirflowConfig

def test_build_training_approval_blocks_initializing():
    no_drift_result = build_training_approval_blocks_initializing(None)
    with_drift_result = build_training_approval_blocks_initializing(
        drift_result=DriftCheckResult(
            drift_summary={
                "data_drift": {},
                "concept_drift": {
                    "average_precision": 1.0,
                    "average_precision_delta": 1.0,
                    "f1": 1.0,
                    "f1_delta": 1.0,
                    "precision": 1.0,
                    "precision_delta": 1.0,
                    "recall": 1.0,
                    "recall_delta": 1.0,
                    "fraud_rate": 1.0,
                    "fraud_rate_delta": 1.0,
                }
            },
            drift_detected=False
        )
    )

    assert no_drift_result[0]["text"]["text"] == "🆕 First Training Required"
    assert with_drift_result[0]["text"]["text"] == "⚠️ Model Retraining Required"

def test_initialize_training_approval(mocker: MockerFixture):
    ts = "value"
    mocker.patch(
        target="dags.shared.services.slack.slack_client.chat_postMessage",
        return_value={"ts": ts}
    )

    output: ModelDeploymentWorkflowForTraining = initialize_training_approval.function(
        model_deployment_workflow_for_training=ModelDeploymentWorkflowForTraining(
            state="value",
            should_train_for_promotion=True,
            id=uuid4(),
            slack_training_approval_message_ts=None,
        ),
        drift_result=DriftCheckResult(
            drift_summary={
                "data_drift": {},
                "concept_drift": {
                    "average_precision": 1.0,
                    "average_precision_delta": 1.0,
                    "f1": 1.0,
                    "f1_delta": 1.0,
                    "precision": 1.0,
                    "precision_delta": 1.0,
                    "recall": 1.0,
                    "recall_delta": 1.0,
                    "fraud_rate": 1.0,
                    "fraud_rate_delta": 1.0,
                }
            },
            drift_detected=True
        )
    )

    assert output.slack_training_approval_message_ts == ts

def test_training_decision_buttons():
    uuid = uuid4()
    should_train_for_promotion = True

    output = training_decision_buttons(
        workflow_id=uuid,
        should_train_for_promotion=should_train_for_promotion
    )

    assert isinstance(output, list)

    for item in output:
        value = json.loads(item["value"])
        assert UUID(value["workflow_id"]) == uuid
        assert value["should_train_for_promotion"] == should_train_for_promotion
        assert value["mwaa_environment_name"] == AirflowConfig.MWAA_ENVIRONMENT_NAME()
        assert value["aws_endpoint_url_mwaa"] == AirflowConfig.AWS_ENDPOINT_URL_MWAA()

def test_build_training_approval_blocks():
    no_drift_result = build_training_approval_blocks(
        workflow_id=uuid4(),
        drift_result=None,
        should_train_for_promotion=True
    )
    with_drift_result = build_training_approval_blocks(
        workflow_id=uuid4(),
        drift_result=DriftCheckResult(
            drift_summary={
                "data_drift": {},
                "concept_drift": {
                    "average_precision": 1.0,
                    "average_precision_delta": 1.0,
                    "f1": 1.0,
                    "f1_delta": 1.0,
                    "precision": 1.0,
                    "precision_delta": 1.0,
                    "recall": 1.0,
                    "recall_delta": 1.0,
                    "fraud_rate": 1.0,
                    "fraud_rate_delta": 1.0,
                }
            },
            drift_detected=False
        ),
        should_train_for_promotion=True
    )

    assert no_drift_result[0]["text"]["text"] == "🆕 First Training Required"
    assert with_drift_result[0]["text"]["text"] == "⚠️ Model Retraining Required"