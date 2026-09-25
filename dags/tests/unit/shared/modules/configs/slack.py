from dags.shared.modules.configs.slack import SlackConfig

class TestSlackConfig:
    def test_values(self):
        assert isinstance(SlackConfig.SLACK_CHANNEL_ID(), str)
        assert isinstance(SlackConfig.SLACK_CONNECTION_ID(), str)