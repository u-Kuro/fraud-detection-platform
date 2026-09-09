from dags.model_lifecycle_orchestrator.check_training_need.modules.configs.airflow.task_ids import NoActionTaskIDs, DispatchTrainingApprovalTaskIDs, SetupTrainingApprovalTaskIDs, TaskIDsGroup

class TestNoActionTaskIDs:
    def test_values(self):
        for actual in NoActionTaskIDs:
            assert  f"{TaskIDsGroup.no_action}.{actual.name}" == actual

class TestDispatchTrainingApprovalTaskIDs:
    def test_values(self):
        for actual in DispatchTrainingApprovalTaskIDs:
            assert  f"{TaskIDsGroup.dispatch_training_approval}.{actual.name}" == actual

class TestSetupTrainingApprovalTaskIDs:
    def test_values(self):
        for actual in SetupTrainingApprovalTaskIDs:
            assert f"{TaskIDsGroup.setup_training_approval}.{actual.name}" == actual