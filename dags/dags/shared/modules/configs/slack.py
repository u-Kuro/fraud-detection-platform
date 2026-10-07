from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr, validate_call

@dataclass(frozen=True)
class SlackConfig:
    @classmethod
    @validate_call(validate_return=True)
    def SLACK_CHANNEL_ID(cls) -> StrictStr:
        return Variable.get(cls.SLACK_CHANNEL_ID.__name__)

    @classmethod
    @validate_call(validate_return=True)
    def SLACK_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.SLACK_CONNECTION_ID.__name__)