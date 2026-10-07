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
    def GITHUB_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.GITHUB_CONNECTION_ID.__name__)

    @classmethod
    @validated_lru_cache
    def GITHUB_TOKEN(cls) -> StrictStr:
        return "test" # Not needed for nektos/act