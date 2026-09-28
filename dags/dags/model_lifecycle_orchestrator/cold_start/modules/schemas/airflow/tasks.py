from pydantic import BaseModel, StrictStr

class TransactionInferencesSeed(BaseModel):
    s3_key: StrictStr