from _pytest.monkeypatch import MonkeyPatch

from dags.shared.modules.configs.airflow.airflow import AirflowConfig
from dags.shared.modules.environment.mlflow import MLflowEnvironment

class TestMLflowEnvironment:
    def test_instance(self):
        from dags.shared.modules.environment.mlflow import mlflow_environment

        assert isinstance(mlflow_environment, MLflowEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}MLFLOW_TRACKING_URI",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}MLFLOW_TRACKING_USERNAME",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}MLFLOW_TRACKING_PASSWORD",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}MLFLOW_WORKSPACE",
            value=value
        )

        environment = MLflowEnvironment()

        assert environment.MLFLOW_TRACKING_URI == value
        assert environment.MLFLOW_TRACKING_USERNAME == value
        assert environment.MLFLOW_TRACKING_PASSWORD == value
        assert environment.MLFLOW_WORKSPACE == value
