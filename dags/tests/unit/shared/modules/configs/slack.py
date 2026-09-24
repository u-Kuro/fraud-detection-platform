from dags.shared.modules.configs.slack import SlackConfig

class TestSlackConfig:
    def test_values(self):
        assert isinstance(SlackConfig.slack_channel_id(), str)
        assert isinstance(SlackConfig.slack_connection_id(), str)