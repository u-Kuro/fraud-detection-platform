from _pytest.monkeypatch import MonkeyPatch

from dags.shared.modules.environment.slack import SlackEnvironment

class TestSlackEnvironment:
    def test_instance(self):
        from dags.shared.modules.environment.slack import slack_environment

        assert isinstance(slack_environment, SlackEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name="SLACK_CONNECTION_ID",
            value=value
        )
        monkeypatch.setenv(
            name="SLACK_CHANNEL_ID",
            value=value
        )

        environment = SlackEnvironment()

        assert environment.SLACK_CONNECTION_ID == value
        assert environment.SLACK_CHANNEL_ID == value