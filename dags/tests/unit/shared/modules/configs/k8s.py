from dags.shared.modules.configs.k8s import K8sConfig

class TestK8sConfig:
    def test_values(self):
        assert isinstance(K8sConfig.k8s_base_config_map_name(), str)
        assert isinstance(K8sConfig.k8s_base_secret_name(), str)
        assert isinstance(K8sConfig.k8s_connection_id(), str)
        assert isinstance(K8sConfig.k8s_docker_registry_secret_name(), str)
        assert isinstance(K8sConfig.k8s_namespace(), str)