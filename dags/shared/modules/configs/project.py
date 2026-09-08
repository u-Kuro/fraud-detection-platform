from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ProjectConfig:
    project_name: str = "fraud_detection_platform"
    root_path: Path = Path(__file__).parents[4]
    dags_path: Path = root_path / "dags"