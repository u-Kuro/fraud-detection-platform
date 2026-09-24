from uuid import uuid4

from dags.model_lifecycle_orchestrator.on_training_decision.modules.schemas.airflow.tasks import ModelDeploymentWorkflowForTraining, TrainingDecision, ModelDeploymentWorkflowForPromotion

class TestModelDeploymentWorkflowForTraining:
    @staticmethod
    def make_workflow(**overrides) -> dict:
        data = {
            "id": uuid4(),
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_workflow()
        values = ModelDeploymentWorkflowForTraining(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual

class TestTrainingDecision:
    def test_values(self):
        approved = True
        workflow_for_training_data = TestModelDeploymentWorkflowForTraining.make_workflow()
        values = TrainingDecision(
            approved=approved,
            model_deployment_workflow=ModelDeploymentWorkflowForTraining(**workflow_for_training_data)
        )

        assert values.approved == approved

        for key, expected in workflow_for_training_data.items():
            actual = getattr(values.model_deployment_workflow, key)

            assert expected == actual

class TestModelDeploymentWorkflowForPromotion:
    @staticmethod
    def make_workflow(**overrides) -> dict:
        data = {
            "slack_promotion_approval_message_ts": "value",
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_workflow()
        values = ModelDeploymentWorkflowForPromotion(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual