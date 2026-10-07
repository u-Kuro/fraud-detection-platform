from dataclasses import dataclass
from uuid import UUID

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class PostgresConfig:
    @classmethod
    @validate_call(validate_return=True)
    def POSTGRES_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.POSTGRES_CONNECTION_ID.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def project_id(cls) -> UUID:
        from dags.shared.modules.configs.project import ProjectConfig
        from dags.shared.repositories.postgres.projects import get_project_id

        return get_project_id(ProjectConfig.project_name)