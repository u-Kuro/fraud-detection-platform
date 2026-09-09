import json

import pytest
from pytest_mock import MockerFixture

from dags.model_lifecycle_orchestrator.check_training_need.modules.configs.airflow.xcom import DriftCheckXComKeys
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.xcom import DriftCheckResult
from dags.shared.modules.schemas.airflow import TaskContext
from tests.dags.unit.shared.modules.schemas.airflow import TestTaskContext

class TestDriftCheckResult:
    @staticmethod
    @pytest.fixture
    def mocked_task_context(mocker: MockerFixture) -> TaskContext:
        xcom_values = {
            DriftCheckXComKeys.drift_detected: True,
            DriftCheckXComKeys.drift_summary: "value",
        }

        task_context = TaskContext(TestTaskContext().make_context())
        task_context.task_instance = mocker.MagicMock()
        task_context.task_instance.xcom_pull.side_effect = lambda **kwargs: xcom_values[kwargs["key"]]

        return task_context

    def test_parse_xcom(self, mocked_task_context: TaskContext):
        output = DriftCheckResult.model_validate(mocked_task_context)

        assert isinstance(output, DriftCheckResult)