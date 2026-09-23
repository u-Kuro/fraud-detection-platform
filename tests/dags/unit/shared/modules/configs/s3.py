from dags.shared.modules.configs.s3 import S3Config

class TestS3Config:
    def test_values(self):
        assert isinstance(S3Config.s3_bucket(), str)
        assert isinstance(S3Config.s3_connection_id(), str)