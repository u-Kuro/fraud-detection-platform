from dags_shared.modules.configs.mlflow import MLflowConfig

class TestMLflowConfig:
    def test_values(self):
        assert isinstance(MLflowConfig.challenger_alias, str)
