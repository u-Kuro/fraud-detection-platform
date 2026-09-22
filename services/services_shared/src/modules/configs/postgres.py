from dataclasses import dataclass
from uuid import UUID

from services_shared.src.modules.configs.project import ProjectConfig
from services_shared.src.repositories.postgres.projects import get_project_id

@dataclass(frozen=True)
class PostgresConfig:
    project_id: UUID = get_project_id(ProjectConfig.project_name)