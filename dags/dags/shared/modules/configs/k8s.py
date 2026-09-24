from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class K8sConfig:
    @classmethod
    @validated_lru_cache
    def k8s_base_config_map_name(cls) -> StrictStr:
        return Variable.get(cls.k8s_base_config_map_name.__name__)

    @classmethod
    @validated_lru_cache
    def k8s_base_secret_name(cls) -> StrictStr:
        return Variable.get(cls.k8s_base_secret_name.__name__)

    @classmethod
    @validated_lru_cache
    def k8s_connection_id(cls) -> StrictStr:
        return Variable.get(cls.k8s_connection_id.__name__)

    @classmethod
    @validated_lru_cache
    def k8s_docker_registry_secret_name(cls) -> StrictStr:
        return Variable.get(cls.k8s_docker_registry_secret_name.__name__)

    @classmethod
    @validated_lru_cache
    def k8s_namespace(cls) -> StrictStr:
        return Variable.get(cls.k8s_namespace.__name__)