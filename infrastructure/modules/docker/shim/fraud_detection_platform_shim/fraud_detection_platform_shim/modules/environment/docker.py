from pydantic_settings import BaseSettings, SettingsConfigDict

class DockerEnvironment(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    SCRIPT_DIRECTORY: str
    ACT_IMAGE: str

docker_environment = DockerEnvironment()