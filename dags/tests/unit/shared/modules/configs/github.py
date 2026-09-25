from dags.shared.modules.configs.github import GitHubConfig

class TestGitHubConfig:
    def test_values(self):
        assert isinstance(GitHubConfig.owner, str)
        assert isinstance(GitHubConfig.repository, str)
        assert isinstance(GitHubConfig.GITHUB_CONNECTION_ID(), str)
        assert isinstance(GitHubConfig.GITHUB_TOKEN(), str)