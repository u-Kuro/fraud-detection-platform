from dags.model_lifecycle_orchestrator.check_training_need.modules.configs.airflow.task_ids import NoActionTaskIDs, DispatchTrainingApprovalTaskIDs, SetupTrainingApprovalTaskIDs
from dags.model_lifecycle_orchestrator.check_training_need.services.tasks import no_action, dispatch_training_approval, setup_training_approval

class TestNoActionTaskIDs:
    def test_values(self):
        for actual in NoActionTaskIDs:
            assert  f"{no_action.__name__}.{actual.name}" == actual

class TestDispatchTrainingApprovalTaskIDs:
    def test_values(self):
        for actual in DispatchTrainingApprovalTaskIDs:
            assert  f"{dispatch_training_approval.__name__}.{actual.name}" == actual

class TestSetupTrainingApprovalTaskIDs:
    def test_values(self):
        for actual in SetupTrainingApprovalTaskIDs:
            assert f"{setup_training_approval.__name__}.{actual.name}" == actual