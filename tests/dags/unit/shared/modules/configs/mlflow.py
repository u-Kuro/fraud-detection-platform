from dags.shared.modules.configs.mlflow import MLflowConfig

class TestMLflowConfig:
    def test_values(self):
        assert isinstance(MLflowConfig.challenger_alias, str)
        assert isinstance(MLflowConfig.mlflow_tracking_uri(), str)
        assert isinstance(MLflowConfig.mlflow_tracking_username(), str)
        assert isinstance(MLflowConfig.mlflow_tracking_password(), str)
        assert isinstance(MLflowConfig.mlflow_workspace(), str)
