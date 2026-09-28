from _pytest.monkeypatch import MonkeyPatch

from shared.modules.environment.s3 import S3Environment

class TestS3Environment:
    def test_instance(self):
        from shared.modules.environment.s3 import s3_environment

        assert isinstance(s3_environment, S3Environment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(name="AWS_DEFAULT_REGION", value=value)
        monkeypatch.setenv(name="AWS_ENDPOINT_URL_S3", value=value)
        monkeypatch.setenv(name="AWS_ACCESS_KEY_ID", value=value)
        monkeypatch.setenv(name="AWS_SECRET_ACCESS_KEY", value=value)
        monkeypatch.setenv(name="S3_BUCKET_NAME", value=value)

        environment = S3Environment()

        assert environment.AWS_DEFAULT_REGION == value
        assert environment.AWS_ENDPOINT_URL_S3 == value
        assert environment.AWS_ACCESS_KEY_ID == value
        assert environment.AWS_SECRET_ACCESS_KEY == value
        assert environment.S3_BUCKET_NAME == value