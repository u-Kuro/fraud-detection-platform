from _pytest.monkeypatch import MonkeyPatch

from dags.shared.modules.configs.airflow.airflow import AirflowConfig
from dags.shared.modules.environment.postgres import PostgresEnvironment

class TestPostgresEnvironment:
    def test_instance(self):
        from dags.shared.modules.environment.postgres import postgres_environment

        assert isinstance(postgres_environment, PostgresEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}POSTGRES_CONNECTION_ID",
            value=value
        )

        environment = PostgresEnvironment()

        assert environment.POSTGRES_CONNECTION_ID == value