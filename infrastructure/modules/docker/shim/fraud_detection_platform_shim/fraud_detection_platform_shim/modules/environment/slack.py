from pydantic import StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class SlackEnvironment(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
    )

    SLACK_APP_LEVEL_TOKEN: StrictStr
    SLACK_BOT_USER_OAUTH_TOKEN: StrictStr
    SLACK_SIGNING_SECRET: StrictStr

slack_environment = SlackEnvironment()