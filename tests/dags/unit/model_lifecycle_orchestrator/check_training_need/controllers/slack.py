import json
from uuid import uuid4, UUID

from pytest_mock import MockerFixture

from dags.model_lifecycle_orchestrator.check_training_need.controllers.slack import build_training_approval_blocks_initializing, initialize_training_approval, cold_start_buttons, drift_retraining_buttons, build_training_approval_blocks
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.tasks import ModelDeploymentWorkflowForTraining
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.xcom import DriftCheckResult

def test_build_training_approval_blocks_initializing():
    no_drift_result = build_training_approval_blocks_initializing(None)
    with_drift_result = build_training_approval_blocks_initializing(
        drift_result=DriftCheckResult(
            drift_summary={"value":{}},
            drift_detected=False
        )
    )

    assert no_drift_result[0]["text"]["text"] == "🆕 Training Required"
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
            drift_summary={"value": {}},
            drift_detected=True
        )
    )

    assert output.slack_training_approval_message_ts == ts

def test_cold_start_buttons():
    uuid = uuid4()
    should_train_for_promotion = True

    output = cold_start_buttons(
        workflow_id=uuid,
        should_train_for_promotion=should_train_for_promotion
    )

    assert isinstance(output, list)

    for item in output:
        value = json.loads(item["value"])
        assert UUID(value["workflow_id"]) == uuid
        assert value["should_train_for_promotion"] == should_train_for_promotion

def test_drift_retraining_buttons():
    uuid = uuid4()
    should_train_for_promotion = True

    output = drift_retraining_buttons(
        workflow_id=uuid,
        should_train_for_promotion=should_train_for_promotion
    )

    assert isinstance(output, list)

    for item in output:
        value = json.loads(item["value"])
        assert UUID(value["workflow_id"]) == uuid
        assert value["should_train_for_promotion"] == should_train_for_promotion

def test_build_training_approval_blocks():
    no_drift_result = build_training_approval_blocks(
        workflow_id=uuid4(),
        drift_result=None,
        should_train_for_promotion=True
    )
    with_drift_result = build_training_approval_blocks(
        workflow_id=uuid4(),
        drift_result=DriftCheckResult(
            drift_summary={"value":{}},
            drift_detected=False
        ),
        should_train_for_promotion=True
    )

    assert no_drift_result[0]["text"]["text"] == "🆕 Training Required"
    assert with_drift_result[0]["text"]["text"] == "⚠️ Model Retraining Required"