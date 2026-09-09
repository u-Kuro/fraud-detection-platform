import json
from datetime import datetime
from uuid import uuid4, UUID

from pytest_mock import MockerFixture

from dags.model_lifecycle_orchestrator.on_training_decision.controllers.slack import initialize_promotion_approval, model_promotion_buttons
from dags.model_lifecycle_orchestrator.on_training_decision.modules.schemas.airflow.tasks import ModelDeploymentWorkflowForPromotion
from dags.model_lifecycle_orchestrator.on_training_decision.modules.schemas.airflow.xcom import TrainModelResult

def test_initialize_promotion_approval(mocker: MockerFixture):
    ts = "value"
    mocker.patch(
        target="dags.shared.services.slack.slack_client.chat_postMessage",
        return_value={"ts": ts}
    )

    output: ModelDeploymentWorkflowForPromotion = initialize_promotion_approval.function(
        train_model_result=TrainModelResult(
            model_trained_at_datetime=datetime.now(),
            model_mlflow_run_id="value",
            model_name="value",
            model_version=1,
            model_dataset_min_datetime=datetime.now(),
            model_dataset_max_datetime=datetime.now(),
            model_f1_score=1.0,
            model_pr_auc=1.0,
            model_recall=1.0,
            model_precision=1.0
        )
    )

    assert output.slack_promotion_approval_message_ts == ts

def test_model_promotion_buttons():
    uuid = uuid4()

    output = model_promotion_buttons(
        workflow_id=uuid,
    )

    assert isinstance(output, list)

    for item in output:
        value = json.loads(item["value"])
        assert UUID(value["workflow_id"]) == uuid