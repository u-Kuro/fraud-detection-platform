from uuid import UUID

from dags_shared.modules.configs.postgres import PostgresConfig

class TestPostgresConfig:
    def test_values(self):
        assert isinstance(PostgresConfig.project_id, UUID)
