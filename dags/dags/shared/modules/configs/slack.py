from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_cache

@dataclass(frozen=True)
class SlackConfig:
    @classmethod
    @validated_cache
    def SLACK_CHANNEL_ID(cls) -> StrictStr:
        return Variable.get(cls.SLACK_CHANNEL_ID.__name__)

    @classmethod
    @validated_cache
    def SLACK_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.SLACK_CONNECTION_ID.__name__)