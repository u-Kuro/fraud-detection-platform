from datetime import datetime

import pytest
from train_model.modules.schemas.postgres.model_deployment_workflows import ModelDeploymentWorkflowDatasetTimestamps

class TestModelDeploymentWorkflowDatasetTimestamps:
    @staticmethod
    @pytest.fixture
    def data() -> dict:
        return {
            "model_dataset_min_iso_datetime": datetime.now().isoformat(),
            "model_dataset_max_iso_datetime": datetime.now().isoformat(),
        }

    def test_values(self, data: dict):
        values = ModelDeploymentWorkflowDatasetTimestamps(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual