from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ProjectConfig:
    dags_path: Path = Path(__file__).parents[3]
    project_name: str = "fraud_detection_platform"