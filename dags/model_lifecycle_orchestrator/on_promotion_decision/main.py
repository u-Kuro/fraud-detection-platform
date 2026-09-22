from airflow.sdk import dag

from model_lifecycle_orchestrator.on_promotion_decision.repositories.postgres.model_deployment_workflows import update_approved_promotion_workflow, delete_rejected_promotion_workflow
from model_lifecycle_orchestrator.on_promotion_decision.repositories.postgres.model_deployments import promote_model_deployment
from model_lifecycle_orchestrator.on_promotion_decision.services.tasks import check_promotion_decision, get_promotion_decision, apply_model_deployment, archive_transaction_inferences_used_for_deployed_model, get_transaction_inferences_iso_datetime_cutoff
from dags_shared.modules.configs.airflow.dag_ids import DAGIDs
from dags_shared.modules.configs.project import ProjectConfig
from dags_shared.modules.utilities.airflow.airflow import sequence
from dags_shared.services.slack import slack_failure_alert

@dag(
    dag_id=DAGIDs.on_promotion_decision,
    max_active_runs=1,
    default_args={
        "on_failure_callback": slack_failure_alert
    },
    is_paused_upon_creation=False,
    tags=[ProjectConfig.project_name, "triggered", "promotion", "decision"]
)
def on_promotion_decision():
    sequence(
        promotion_decision := get_promotion_decision(),
        check_promotion_decision(promotion_decision),
        [
            sequence(
                update_approved_promotion_workflow(promotion_decision),
                promoted_model_deployment := promote_model_deployment(promotion_decision),
                transaction_inferences_iso_datetime_cutoff := get_transaction_inferences_iso_datetime_cutoff(promoted_model_deployment),
                apply_model_deployment(),
                archive_transaction_inferences_used_for_deployed_model(transaction_inferences_iso_datetime_cutoff)
            ),

            delete_rejected_promotion_workflow(promotion_decision)
        ]
    )

on_promotion_decision()