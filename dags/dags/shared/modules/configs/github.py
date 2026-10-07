from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class GitHubConfig:
    owner: str = "u-Kuro"
    repository: str = "fraud_detection_platform"

    @classmethod
    @validate_call(validate_return=True)
    def GITHUB_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.GITHUB_CONNECTION_ID.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def GITHUB_TOKEN(cls) -> StrictStr:
        return "test" # Not needed for nektos/act