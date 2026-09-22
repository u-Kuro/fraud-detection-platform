from datetime import datetime
from uuid import uuid4

from model_lifecycle_orchestrator.on_promotion_decision.modules.schemas.airflow.tasks import ModelDeploymentWorkflowForPromotion, PromotionDecision, PromotedModelDeployment

class TestModelDeploymentWorkflowForPromotion:
    @staticmethod
    def make_workflow(**overrides) -> dict:
        data = {
            "id": uuid4(),
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_workflow()
        values = ModelDeploymentWorkflowForPromotion(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual

class TestPromotionDecision:
    def test_values(self):
        approved = True
        workflow_for_promotion_data = TestModelDeploymentWorkflowForPromotion.make_workflow()
        values = PromotionDecision(
            approved=approved,
            model_deployment_workflow=ModelDeploymentWorkflowForPromotion(**workflow_for_promotion_data)
        )

        assert values.approved == approved

        for key, expected in workflow_for_promotion_data.items():
            actual = getattr(values.model_deployment_workflow, key)

            assert expected == actual

class TestPromotedModelDeployment:
    @staticmethod
    def make_deployment(**overrides) -> dict:
        data = {
            "dataset_max_timestamp": datetime.now(),
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_deployment()
        values = PromotedModelDeployment(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual