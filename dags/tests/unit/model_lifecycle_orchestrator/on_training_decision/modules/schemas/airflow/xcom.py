from datetime import datetime

import pytest
from pytest_mock import MockerFixture

from dags.model_lifecycle_orchestrator.on_training_decision.modules.configs.airflow.xcom import TrainModelXComKeys
from dags.model_lifecycle_orchestrator.on_training_decision.modules.schemas.airflow.xcom import TrainModelResult
from dags.shared.modules.schemas.airflow import TaskContext
from tests.unit.shared.modules.schemas.airflow import TestTaskContext

class TestTrainModelResult:
    @staticmethod
    @pytest.fixture
    def mocked_task_context(mocker: MockerFixture) -> TaskContext:
        xcom_values = {
            TrainModelXComKeys.model_trained_at_datetime: datetime.now(),
            TrainModelXComKeys.model_mlflow_run_id: "value",
            TrainModelXComKeys.model_name: "value",
            TrainModelXComKeys.model_version: 1,
            TrainModelXComKeys.model_dataset_min_datetime: datetime.now(),
            TrainModelXComKeys.model_dataset_max_datetime: datetime.now(),
            TrainModelXComKeys.model_f1_score: 1.0,
            TrainModelXComKeys.model_pr_auc: 1.0,
            TrainModelXComKeys.model_recall: 1.0,
            TrainModelXComKeys.model_precision: 1.0,
        }

        task_context = TaskContext(TestTaskContext().make_context())
        task_context.task_instance = mocker.MagicMock()
        task_context.task_instance.xcom_pull.side_effect = lambda **kwargs: xcom_values[kwargs["key"]]

        return task_context

    def test_parse_xcom(self, mocked_task_context: TaskContext):
        output = TrainModelResult.model_validate(mocked_task_context)

        assert isinstance(output, TrainModelResult)