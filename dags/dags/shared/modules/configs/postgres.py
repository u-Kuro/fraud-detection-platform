from dataclasses import dataclass
from uuid import UUID

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.configs.project import ProjectConfig
from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache
from dags.shared.repositories.postgres.projects import get_project_id

@dataclass(frozen=True)
class PostgresConfig:
    @classmethod
    @validated_lru_cache
    def postgres_connection_id(cls) -> StrictStr:
        return Variable.get(cls.postgres_connection_id.__name__)

    @classmethod
    @validated_lru_cache
    def project_id(cls) -> UUID:
        return get_project_id(ProjectConfig.project_name)