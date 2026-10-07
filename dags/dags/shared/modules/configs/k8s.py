from dataclasses import dataclass

from airflow.sdk import Variable
from pydantic import StrictStr

from dags.shared.modules.utilities.pydantic.pydantic import validated_lru_cache

@dataclass(frozen=True)
class K8sConfig:
    @classmethod
    @validated_lru_cache
    def K8S_BASE_CONFIG_MAP_NAME(cls) -> StrictStr:
        return Variable.get(cls.K8S_BASE_CONFIG_MAP_NAME.__name__)

    @classmethod
    @validated_lru_cache
    def K8S_BASE_SECRET_NAME(cls) -> StrictStr:
        return Variable.get(cls.K8S_BASE_SECRET_NAME.__name__)

    @classmethod
    @validated_lru_cache
    def K8S_CONNECTION_ID(cls) -> StrictStr:
        return Variable.get(cls.K8S_CONNECTION_ID.__name__)

    @classmethod
    @validated_lru_cache
    def K8S_DOCKER_REGISTRY_SECRET_NAME(cls) -> StrictStr:
        return Variable.get(cls.K8S_DOCKER_REGISTRY_SECRET_NAME.__name__)

    @classmethod
    @validated_lru_cache
    def K8S_NAMESPACE(cls) -> StrictStr:
        return Variable.get(cls.K8S_NAMESPACE.__name__)