from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class SlackConfig:
    @classmethod
    @validated_lru_cache
    def slack_channel_id(cls) -> StrictStr:
        return Variable.get(cls.slack_channel_id.__name__)

    @classmethod
    @validated_lru_cache
    def slack_connection_id(cls) -> StrictStr:
        return Variable.get(cls.slack_connection_id.__name__)