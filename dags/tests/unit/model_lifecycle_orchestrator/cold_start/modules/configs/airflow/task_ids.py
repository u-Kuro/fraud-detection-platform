from dags.model_lifecycle_orchestrator.cold_start.modules.configs.airflow.task_ids import NoActionTaskIDs, TaskIDsGroup

class TestNoActionTaskIDs:
    def test_values(self):
        for actual in NoActionTaskIDs:
            assert  f"{TaskIDsGroup.no_action}-{actual.name}" == actual