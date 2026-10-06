from pydantic import StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class DockerEnvironment(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    ACT_IMAGE: StrictStr
    SCRIPT_DIRECTORY: StrictStr

docker_environment = DockerEnvironment()