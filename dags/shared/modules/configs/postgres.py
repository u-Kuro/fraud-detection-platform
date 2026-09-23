from dataclasses import dataclass
from uuid import UUID

from dags.shared.modules.configs.project import ProjectConfig
from dags.shared.repositories.postgres.projects import get_project_id

@dataclass(frozen=True)
class PostgresConfig:
    project_id: UUID = get_project_id(ProjectConfig.project_name)