from _pytest.monkeypatch import MonkeyPatch

from shared.modules.environment.postgres import PostgresEnvironment

class TestPostgresEnvironment:
    def test_instance(self):
        from shared.modules.environment.postgres import postgres_environment

        assert isinstance(postgres_environment, PostgresEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(name="PGHOST", value=value)
        monkeypatch.setenv(name="PGPORT", value=value)
        monkeypatch.setenv(name="PGDATABASE", value=value)
        monkeypatch.setenv(name="PGUSER", value=value)
        monkeypatch.setenv(name="PGPASSWORD", value=value)

        environment = PostgresEnvironment()

        assert environment.PGHOST == value
        assert environment.PGPORT == value
        assert environment.PGDATABASE == value
        assert environment.PGUSER == value
        assert environment.PGPASSWORD == value
