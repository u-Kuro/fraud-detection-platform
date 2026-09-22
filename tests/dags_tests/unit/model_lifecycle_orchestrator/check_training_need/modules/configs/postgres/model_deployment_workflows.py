from model_lifecycle_orchestrator.check_training_need.modules.configs.postgres.model_deployment_workflows import ModelDeploymentWorkflowsConfig, ReservedModelDeploymentWorkflowLabels, ExpiredModelDeploymentWorkflowsLabels
from dags_shared.modules.schemas.postgres.model_deployment_workflows import ModelDeploymentWorkflows

class TestModelDeploymentWorkflowsConfig:
    def test_values(self):
        assert isinstance(ModelDeploymentWorkflowsConfig.challenger_model_expiration_days, int)
        assert ModelDeploymentWorkflowsConfig.challenger_model_expiration_days >= 1

class TestReservedModelDeploymentWorkflowLabels:
    def test_values(self):
        for actual in ReservedModelDeploymentWorkflowLabels:
            assert f"reserved_{ModelDeploymentWorkflows.__tablename__}_{actual.name}" == actual

class TestExpiredModelDeploymentWorkflowsLabels:
    def test_values(self):
        for actual in ExpiredModelDeploymentWorkflowsLabels:
            assert f"expired_{ModelDeploymentWorkflows.__tablename__}_{actual.name}" == actual