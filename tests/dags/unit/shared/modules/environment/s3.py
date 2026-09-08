from _pytest.monkeypatch import MonkeyPatch

from dags.shared.modules.environment.s3 import S3Environment

class TestS3Environment:
    def test_instance(self):
        from dags.shared.modules.environment.s3 import s3_environment

        assert isinstance(s3_environment, S3Environment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name="S3_CONNECTION_ID",
            value=value
        )
        monkeypatch.setenv(
            name="S3_BUCKET",
            value=value
        )

        environment = S3Environment()

        assert environment.S3_CONNECTION_ID == value
        assert environment.S3_BUCKET == value