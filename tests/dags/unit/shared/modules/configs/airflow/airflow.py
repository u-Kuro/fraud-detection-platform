from dags.shared.modules.configs.airflow.airflow import AirflowConfig

class TestAirflowConfig:
    def test_values(self):
        assert isinstance(AirflowConfig.environment_prefix, str)
        assert AirflowConfig.environment_prefix == "AIRFLOW_VAR_"