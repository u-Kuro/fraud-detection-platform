from uuid import UUID

from services.shared.src.modules.configs.postgres import PostgresConfig

class TestPostgresConfig:
    def test_values(self):
        result = PostgresConfig.project_id
        assert isinstance(result, UUID)