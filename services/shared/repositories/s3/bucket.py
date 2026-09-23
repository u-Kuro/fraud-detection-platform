from shared.repositories.s3.s3 import s3_client

def ensure_bucket(bucket_name: str) -> None:
    if not s3_client.check_for_bucket(bucket_name=bucket_name):
        s3_client.create_bucket(bucket_name=bucket_name)