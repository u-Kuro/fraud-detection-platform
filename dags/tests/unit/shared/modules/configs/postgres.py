from uuid import UUID

from dags.shared.modules.configs.postgres import PostgresConfig

class TestPostgresConfig:
    def test_values(self):
        assert isinstance(PostgresConfig.postgres_connection_id(), str)
        assert isinstance(PostgresConfig.project_id(), UUID)
