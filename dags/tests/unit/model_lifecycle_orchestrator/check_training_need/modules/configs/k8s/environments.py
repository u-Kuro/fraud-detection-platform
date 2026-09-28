from dags.model_lifecycle_orchestrator.check_training_need.modules.configs.k8s.environments import DriftCheckEnvironmentKeys

class TestDriftCheckEnvironmentKeys:
    def test_identity(self):
        from enum import StrEnum
        assert issubclass(DriftCheckEnvironmentKeys, StrEnum)

    def test_active_model_deployment_mlflow_run_id(self):
        assert DriftCheckEnvironmentKeys.ACTIVE_MODEL_DEPLOYMENT_MLFLOW_RUN_ID == "ACTIVE_MODEL_DEPLOYMENT_MLFLOW_RUN_ID"