from dags.shared.modules.configs.s3 import S3Config

class TestS3Config:
    def test_values(self):
        assert isinstance(S3Config.S3_BUCKET(), str)
        assert isinstance(S3Config.S3_CONNECTION_ID(), str)