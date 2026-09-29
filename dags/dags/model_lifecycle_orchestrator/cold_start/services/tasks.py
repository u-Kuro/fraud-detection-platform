from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import task, get_current_context
from kubernetes.client import models

from dags.model_lifecycle_orchestrator.cold_start.modules.configs.airflow.task_ids import NoActionTaskIDs
from dags.model_lifecycle_orchestrator.cold_start.modules.configs.k8s.environments import SeedTransactionInferencesEnvironmentKeys
from dags.model_lifecycle_orchestrator.cold_start.modules.schemas.airflow.tasks import DataSeeding
from dags.shared.modules.configs.airflow.dag_ids import DAGIDs
from dags.shared.modules.configs.ecr import ECRConfig
from dags.shared.modules.configs.k8s import K8sConfig
from dags.shared.modules.schemas.airflow import TaskContext

def no_action(task_id: NoActionTaskIDs) -> EmptyOperator:
    return EmptyOperator(task_id=task_id)

@task
def get_transaction_inferences_seed_s3_key() -> str:
    context = TaskContext(get_current_context())

    return context.configurations(pydantic_model=DataSeeding).transaction_inferences_seed_s3_key

def seed_transaction_inferences_pod(transaction_inferences_seed_s3_key: str) -> KubernetesPodOperator:
    return KubernetesPodOperator(
        task_id=seed_transaction_inferences_pod.__name__,
        name=seed_transaction_inferences_pod.__name__,
        namespace=K8sConfig.K8S_NAMESPACE(),
        kubernetes_conn_id=K8sConfig.K8S_CONNECTION_ID(),
        image=ECRConfig.SEED_TRANSACTION_INFERENCES_IMAGE(),
        image_pull_policy="Always",
        image_pull_secrets=[
            models.V1LocalObjectReference(
                name=K8sConfig.K8S_DOCKER_REGISTRY_SECRET_NAME()
            )
        ],
        env_vars=[
            models.V1EnvVar(
                name=SeedTransactionInferencesEnvironmentKeys.TRANSACTION_INFERENCES_SEED_S3_KEY,
                value=transaction_inferences_seed_s3_key
            )
        ],
        env_from=[
            models.V1EnvFromSource(
                config_map_ref=models.V1ConfigMapEnvSource(
                    name=K8sConfig.K8S_BASE_CONFIG_MAP_NAME()
                )
            ),
            models.V1EnvFromSource(
                secret_ref=models.V1SecretEnvSource(
                    name=K8sConfig.K8S_BASE_SECRET_NAME()
                )
            ),
        ],
        do_xcom_push=False,
        startup_timeout_seconds=300,
        get_logs=True,
        log_events_on_failure=True,
        on_finish_action="delete_pod",
    )

def trigger_check_training_need() -> TriggerDagRunOperator:
    return TriggerDagRunOperator(
        task_id=trigger_check_training_need.__name__,
        trigger_dag_id=DAGIDs.check_training_need,
        wait_for_completion=True,
    )