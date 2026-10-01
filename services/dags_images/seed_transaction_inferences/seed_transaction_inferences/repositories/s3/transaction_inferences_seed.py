import tempfile
from typing import Iterator

import pandas
from pandas import DataFrame

from shared.modules.environment.s3 import s3_environment

from seed_transaction_inferences.modules.environment.seed_transaction_inferences import seed_transaction_inferences_environment
from shared.repositories.s3.s3 import s3_client

def get_transaction_inferences_seed_iterator() -> Iterator[DataFrame]:
    with tempfile.TemporaryFile() as file:
        s3_client.download_fileobj(
            Bucket=s3_environment.S3_BUCKET_NAME,
            Key=seed_transaction_inferences_environment.TRANSACTION_INFERENCES_SEED_S3_KEY,
            Fileobj=file,
        )
        file.seek(0)

        with pandas.read_csv(
            filepath_or_buffer=file,
            compression="gzip",
            dtype={
                "Time": "float64",
                **{f"V{i}": "float64" for i in range(1, 29)},
                "Amount": "float64",
                "Class": "int8",
            },
            chunksize=2_000, # For current low resource
        ) as reader:
            yield from reader