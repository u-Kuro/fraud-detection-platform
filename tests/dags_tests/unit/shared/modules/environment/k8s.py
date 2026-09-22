from _pytest.monkeypatch import MonkeyPatch

from dags_shared.modules.configs.airflow.airflow import AirflowConfig
from dags_shared.modules.environment.k8s import K8sEnvironment

class TestK8sEnvironment:
    def test_instance(self):
        from dags_shared.modules.environment.k8s import k8s_environment

        assert isinstance(k8s_environment, K8sEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}K8S_CONNECTION_ID",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}K8S_NAMESPACE",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}K8S_BASE_CONFIG_MAP_NAME",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}K8S_BASE_SECRET_NAME",
            value=value
        )
        monkeypatch.setenv(
            name=f"{AirflowConfig.environment_prefix}K8S_DOCKER_REGISTRY_SECRET_NAME",
            value=value
        )

        environment = K8sEnvironment()

        assert environment.K8S_CONNECTION_ID == value
        assert environment.K8S_NAMESPACE == value
        assert environment.K8S_BASE_CONFIG_MAP_NAME == value
        assert environment.K8S_BASE_SECRET_NAME == value
        assert environment.K8S_DOCKER_REGISTRY_SECRET_NAME == value
