from pathlib import Path

from dags_shared.modules.configs.project import ProjectConfig

class TestProjectConfig:
    def test_values(self):
        assert isinstance(ProjectConfig.project_name, str)
        assert isinstance(ProjectConfig.dags_path, Path)
