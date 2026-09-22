from uuid import uuid4

from model_lifecycle_orchestrator.check_training_need.modules.schemas.model_deployment_workflows import ModelDeploymentWorkflow
from dags_shared.modules.schemas.postgres.model_deployment_workflows import ModelDeploymentWorkflowState

class TestModelDeploymentWorkflow:
    @staticmethod
    def make_workflow(**overrides) -> dict:
        data = {
            "id": uuid4(),
            "state": ModelDeploymentWorkflowState.train_pending,
            "slack_training_approval_message_ts": "value",
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_workflow()
        values = ModelDeploymentWorkflow(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual