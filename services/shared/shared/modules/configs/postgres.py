from dataclasses import dataclass
from uuid import UUID

from shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class PostgresConfig:
    @classmethod
    @validated_lru_cache
    def project_id(cls) -> UUID:
        from shared.modules.configs.project import ProjectConfig
        from shared.repositories.postgres.projects import get_project_id

        return get_project_id(ProjectConfig.project_name)