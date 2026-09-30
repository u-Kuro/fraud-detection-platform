from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from botocore.config import Config

from dags.shared.modules.configs.s3 import S3Config

s3_hook = S3Hook(
    aws_conn_id=S3Config.S3_CONNECTION_ID(),
    config=Config(
        inject_host_prefix=False,
        request_checksum_calculation="when_required",
        s3={"addressing_style": "path"},
    )
)