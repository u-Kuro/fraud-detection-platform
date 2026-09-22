from _pytest.monkeypatch import MonkeyPatch

from dags_shared.modules.configs.airflow.airflow import AirflowConfig
from dags_shared.modules.environment.github import GitHubEnvironment

class TestGitHubEnvironment:
    def test_instance(self):
        from dags_shared.modules.environment.github import github_environment

        assert isinstance(github_environment, GitHubEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}GITHUB_CONNECTION_ID",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}GITHUB_TOKEN",
            value=value
        )

        environment = GitHubEnvironment()

        assert environment.GITHUB_CONNECTION_ID == value
        assert environment.GITHUB_TOKEN == value