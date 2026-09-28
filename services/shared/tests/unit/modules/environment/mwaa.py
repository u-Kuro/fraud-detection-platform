from _pytest.monkeypatch import MonkeyPatch

from shared.modules.environment.mwaa import MWAAEnvironment

class TestMWAAEnvironment:
    def test_instance(self):
        from shared.modules.environment.mwaa import mwaa_environment

        assert isinstance(mwaa_environment, MWAAEnvironment)

    def test_mwaa_environment_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(name="AWS_DEFAULT_REGION", value=value)
        monkeypatch.setenv(name="AWS_ENDPOINT_URL_MWAA", value=value)
        monkeypatch.setenv(name="AWS_ACCESS_KEY_ID", value=value)
        monkeypatch.setenv(name="AWS_SECRET_ACCESS_KEY", value=value)
        monkeypatch.setenv(name="MWAA_ENVIRONMENT_NAME", value=value)

        environment = MWAAEnvironment()

        assert environment.AWS_DEFAULT_REGION == value
        assert environment.AWS_ENDPOINT_URL_MWAA == value
        assert environment.AWS_ACCESS_KEY_ID == value
        assert environment.AWS_SECRET_ACCESS_KEY == value
        assert environment.MWAA_ENVIRONMENT_NAME == value