from pydantic import BaseModel, StrictStr

class DataSeeding(BaseModel):
    transaction_inferences_seed_s3_key: StrictStr