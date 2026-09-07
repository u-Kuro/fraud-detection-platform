from dataclasses import dataclass
from uuid import UUID

from services.shared.src.modules.configs.project import ProjectConfig
from services.shared.src.repositories.postgres.projects import get_project_id

@dataclass(frozen=True)
class PostgresConfig:
    project_id: UUID = get_project_id(ProjectConfig.project_name)