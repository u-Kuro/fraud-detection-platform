import json

from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.sdk import task, get_current_context
from kubernetes.client import models

from dags.model_lifecycle_orchestrator.on_promotion_decision.modules.configs.k8s.environments import ArchiveEnvironmentKeys
from dags.model_lifecycle_orchestrator.on_promotion_decision.modules.schemas.airflow.tasks import PromotionDecision, PromotedModelDeployment
from dags.model_lifecycle_orchestrator.on_promotion_decision.repositories.postgres.model_deployment_workflows import update_approved_promotion_workflow, delete_rejected_promotion_workflow
from dags.shared.modules.configs.ecr import ECRConfig
from dags.shared.modules.configs.github import GitHubConfig
from dags.shared.modules.configs.k8s import K8sConfig
from dags.shared.modules.schemas.airflow import TaskContext

@task
def get_promotion_decision() -> PromotionDecision:
    context = TaskContext(get_current_context())

    return context.configurations(pydantic_model=PromotionDecision)

@task.branch
def check_promotion_decision(promotion_decision: PromotionDecision) -> str:
    context = TaskContext(get_current_context())

    if promotion_decision.approved:
        return context.resolve_task_id(
            task_id=update_approved_promotion_workflow.function.__name__
        )
    else:
        return context.resolve_task_id(
            task_id=delete_rejected_promotion_workflow.function.__name__
        )

def apply_model_deployment() -> HttpOperator:
    return HttpOperator(
        task_id=apply_model_deployment.__name__,
        http_conn_id=GitHubConfig.GITHUB_CONNECTION_ID(),
        endpoint=f"repos/{GitHubConfig.owner}/{GitHubConfig.repository}/actions/workflows/cd-fraud-detection-api.yaml/dispatches",
        method="POST",
        headers={
            "Authorization": f"Bearer {GitHubConfig.GITHUB_TOKEN()}",
            "Accept": "application/vnd.github+json",
        },
        # Data unused for nektos/act
        data=json.dumps({
            "ref": "main"
        }),
        response_check=lambda response: response.status_code == 204,
    )

@task
def get_transaction_inferences_iso_datetime_cutoff(promoted_model_deployment: PromotedModelDeployment) -> str:
    return promoted_model_deployment.dataset_max_timestamp.isoformat()

def archive_transaction_inferences_used_for_deployed_model(transaction_inferences_iso_datetime_cutoff: str):
    return KubernetesPodOperator(
        task_id=archive_transaction_inferences_used_for_deployed_model.__name__,
        name=archive_transaction_inferences_used_for_deployed_model.__name__,
        namespace=K8sConfig.K8S_NAMESPACE(),
        kubernetes_conn_id=K8sConfig.K8S_CONNECTION_ID(),
        image=ECRConfig.ARCHIVE_IMAGE(),
        image_pull_policy="Always",
        image_pull_secrets=[
            models.V1LocalObjectReference(
                name=K8sConfig.K8S_DOCKER_REGISTRY_SECRET_NAME()
            )
        ],
        env_vars=[
            models.V1EnvVar(
                name=ArchiveEnvironmentKeys.TRANSACTION_INFERENCES_ISO_DATETIME_CUTOFF,
                value=transaction_inferences_iso_datetime_cutoff
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