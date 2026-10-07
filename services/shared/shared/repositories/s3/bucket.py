from shared.repositories.s3.s3 import s3_client

def ensure_bucket(bucket_name: str) -> None:
    try: s3_client.head_bucket(Bucket=bucket_name)
    except: s3_client.create_bucket(Bucket=bucket_name)