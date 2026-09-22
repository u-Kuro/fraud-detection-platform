from uuid import uuid4

from model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.tasks import ExpiredModelDeploymentWorkflow, ReservedModelDeploymentWorkflow, ExpiredAndReservedModelDeploymentWorkflows, ActiveModelDeployment, ModelDeploymentWorkflowForTraining

class TestExpiredModelDeploymentWorkflow:
    @staticmethod
    def make_workflow(**overrides) -> dict:
        data = {
            "id": uuid4(),
            "model_name": "value",
            "model_version": 1,
            "mlflow_run_id": "value",
            "slack_promotion_approval_message_ts": "value",
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_workflow()
        values = ExpiredModelDeploymentWorkflow(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual

class TestReservedModelDeploymentWorkflow:
    @staticmethod
    def make_workflow(**overrides) -> dict:
        data = {
            "model_name": "value",
            "model_version": 1,
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_workflow()
        values = ReservedModelDeploymentWorkflow(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual

class TestExpiredAndReservedModelDeploymentWorkflows:
    def test_values(self):
        expired_workflow_data = TestExpiredModelDeploymentWorkflow.make_workflow()
        reserved_workflow_data = TestReservedModelDeploymentWorkflow.make_workflow()
        values = ExpiredAndReservedModelDeploymentWorkflows(
            expired=ExpiredModelDeploymentWorkflow(**expired_workflow_data),
            reserved=ReservedModelDeploymentWorkflow(**reserved_workflow_data)
        )

        for key, expected in expired_workflow_data.items():
            actual = getattr(values.expired, key)

            assert expected == actual

        for key, expected in reserved_workflow_data.items():
            actual = getattr(values.reserved, key)

            assert expected == actual

class TestActiveModelDeployment:
    @staticmethod
    def make_deployment(**overrides) -> dict:
        data = {
            "mlflow_run_id": "value",
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_deployment()
        values = ActiveModelDeployment(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual

class TestModelDeploymentWorkflowForTraining:
    @staticmethod
    def make_deployment(**overrides) -> dict:
        data = {
            "state": "value",
            "should_train_for_promotion": True,
            "id": None,
            "slack_training_approval_message_ts": None,
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_deployment()
        values = ModelDeploymentWorkflowForTraining(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual

    def test_assignment(self):
        data = self.make_deployment()
        values = ModelDeploymentWorkflowForTraining(**data)

        state = "new"
        should_train_for_promotion = False
        uuid = uuid4()
        slack_training_approval_message_ts = "new"

        values.state = state
        values.should_train_for_promotion = should_train_for_promotion
        values.id = uuid
        values.slack_training_approval_message_ts = slack_training_approval_message_ts

        assert values.state == state
        assert values.should_train_for_promotion == should_train_for_promotion
        assert values.id == uuid
        assert values.slack_training_approval_message_ts == slack_training_approval_message_ts


