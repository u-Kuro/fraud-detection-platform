from dags.shared.modules.configs.airflow.airflow import AirflowConfig

class TestAirflowConfig:
    def test_values(self):
        assert isinstance(AirflowConfig.MWAA_ENVIRONMENT_NAME(), str)
        assert isinstance(AirflowConfig.AWS_ENDPOINT_URL_MWAA(), str)