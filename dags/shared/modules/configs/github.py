from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class GitHubConfig:
    owner: str = "u-Kuro"
    repository: str = "fraud_detection_platform"

    @classmethod
    @validated_lru_cache
    def github_connection_id(cls) -> StrictStr:
        return Variable.get(cls.github_connection_id.__name__)

    @classmethod
    @validated_lru_cache
    def github_token(cls) -> StrictStr:
        return "test" # Not needed for nektos/act