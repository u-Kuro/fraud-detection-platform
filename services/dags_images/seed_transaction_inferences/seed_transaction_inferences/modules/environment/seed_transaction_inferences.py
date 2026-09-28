from pydantic import StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class SeedTransactionInferencesEnvironment(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    TRANSACTION_INFERENCES_SEED_S3_KEY: StrictStr

seed_transaction_inferences_environment = SeedTransactionInferencesEnvironment()