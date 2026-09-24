from dags.shared.modules.configs.github import GitHubConfig

class TestGitHubConfig:
    def test_values(self):
        assert isinstance(GitHubConfig.owner, str)
        assert isinstance(GitHubConfig.repository, str)
        assert isinstance(GitHubConfig.github_connection_id(), str)
        assert isinstance(GitHubConfig.github_token(), str)