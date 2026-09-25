from dags.shared.modules.configs.mlflow import MLflowConfig

class TestMLflowConfig:
    def test_values(self):
        assert isinstance(MLflowConfig.challenger_alias, str)
        assert isinstance(MLflowConfig.MLFLOW_TRACKING_URI(), str)
        assert isinstance(MLflowConfig.MLFLOW_TRACKING_USERNAME(), str)
        assert isinstance(MLflowConfig.MLFLOW_TRACKING_PASSWORD(), str)
        assert isinstance(MLflowConfig.MLFLOW_WORKSPACE(), str)
