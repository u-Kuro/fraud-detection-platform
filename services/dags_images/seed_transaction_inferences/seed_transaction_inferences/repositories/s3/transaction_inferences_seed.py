import io

import pandas
from pandas import DataFrame

from seed_transaction_inferences.modules.environment.seed_transaction_inferences import seed_transaction_inferences_environment
from shared.modules.environment.s3 import s3_environment
from shared.repositories.s3.s3 import s3_client

def get_transaction_inferences_seed_csv() -> DataFrame:
    buffer = io.BytesIO()
    s3_client.download_fileobj(
        Bucket=s3_environment.S3_BUCKET_NAME,
        Key=seed_transaction_inferences_environment.TRANSACTION_INFERENCES_SEED_S3_KEY,
        Fileobj=buffer,
    )

    buffer.seek(0)

    return pandas.read_csv(buffer, compression="gzip")