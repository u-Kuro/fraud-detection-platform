from _pytest.monkeypatch import MonkeyPatch

from dags_shared.modules.configs.airflow.airflow import AirflowConfig
from dags_shared.modules.environment.ecr import ECREnvironment

class TestECREnvironment:
    def test_instance(self):
        from dags_shared.modules.environment.ecr import ecr_environment

        assert isinstance(ecr_environment, ECREnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}DRIFT_CHECK_IMAGE",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}TRAIN_MODEL_IMAGE",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}ARCHIVE_IMAGE",
            value=value
        )

        environment = ECREnvironment()

        assert environment.DRIFT_CHECK_IMAGE == value
        assert environment.TRAIN_MODEL_IMAGE == value
        assert environment.ARCHIVE_IMAGE == value