from uuid import UUID

from dags.shared.modules.configs.postgres import PostgresConfig

class TestPostgresConfig:
    def test_values(self):
        assert isinstance(PostgresConfig.POSTGRES_CONNECTION_ID(), str)
        assert isinstance(PostgresConfig.project_id(), UUID)
