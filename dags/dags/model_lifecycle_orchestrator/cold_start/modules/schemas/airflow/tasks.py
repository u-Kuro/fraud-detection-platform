from airflow.sdk.serde import allow_class
from pydantic import BaseModel, StrictStr

class DataSeeding(BaseModel):
    transaction_inferences_seed_s3_key: StrictStr

allow_class(DataSeeding)