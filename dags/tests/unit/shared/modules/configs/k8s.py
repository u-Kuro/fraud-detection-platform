from dags.shared.modules.configs.k8s import K8sConfig

class TestK8sConfig:
    def test_values(self):
        assert isinstance(K8sConfig.K8S_BASE_CONFIG_MAP_NAME(), str)
        assert isinstance(K8sConfig.K8S_BASE_SECRET_NAME(), str)
        assert isinstance(K8sConfig.K8S_CONNECTION_ID(), str)
        assert isinstance(K8sConfig.K8S_DOCKER_REGISTRY_SECRET_NAME(), str)
        assert isinstance(K8sConfig.K8S_NAMESPACE(), str)