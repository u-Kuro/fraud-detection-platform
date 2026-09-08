from uuid import uuid4, UUID

from pytest_mock import MockerFixture

from dags.shared.modules.configs.postgres import PostgresConfig

class TestPostgresConfig:
    def test_values(self, mocker: MockerFixture):
        value = uuid4()
        mocker.patch(
            target="dags.shared.repositories.postgres.projects.get_project_id",
            return_value=value,
        )

        result = PostgresConfig.project_id

        assert isinstance(result, UUID)
        assert PostgresConfig.project_id == value
