from _pytest.monkeypatch import MonkeyPatch

from services_shared.src.modules.environment.mwaa import MWAAEnvironment

class TestMWAAEnvironment:
    def test_instance(self):
        from services_shared.src.modules.environment.mwaa import mwaa_environment

        assert isinstance(mwaa_environment, MWAAEnvironment)

    def test_mwaa_environment_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name="MWAA_ENVIRONMENT_NAME",
            value=value
        )

        environment = MWAAEnvironment()

        assert environment.MWAA_ENVIRONMENT_NAME == value