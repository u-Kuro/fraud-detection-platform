from dataclasses import dataclass
from uuid import UUID

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_cache

@dataclass(frozen=True)
class PostgresConfig:
    @classmethod
    @validated_cache
    def POSTGRES_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.POSTGRES_CONNECTION_ID.__name__)

    @classmethod
    @validated_cache
    def project_id(cls) -> UUID:
        from dags.shared.modules.configs.project import ProjectConfig
        from dags.shared.repositories.postgres.projects import get_project_id

        return get_project_id(ProjectConfig.project_name)