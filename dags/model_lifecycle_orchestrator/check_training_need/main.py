from datetime import datetime

from airflow.sdk import dag

from model_lifecycle_orchestrator.check_training_need.modules.configs.airflow.task_ids import DispatchTrainingApprovalTaskIDs, NoActionTaskIDs
from model_lifecycle_orchestrator.check_training_need.repositories.postgres.model_deployments import has_active_model_deployment, get_active_model_deployment
from model_lifecycle_orchestrator.check_training_need.services.tasks import invalidate_expired_challenger_model, drift_check, has_drift, dispatch_training_approval, no_action
from dags_shared.modules.configs.airflow.dag_ids import DAGIDs
from dags_shared.modules.configs.project import ProjectConfig
from dags_shared.modules.utilities.airflow.airflow import sequence
from dags_shared.services.slack import slack_failure_alert

@dag(
    dag_id=DAGIDs.check_training_need,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    max_active_runs=1,
    catchup=False,
    default_args={
        "on_failure_callback": slack_failure_alert
    },
    is_paused_upon_creation=False,
    tags=[ProjectConfig.project_name, "scheduled", "daily", "monitor", "drift"],
)
def check_training_need():
    sequence(
        invalidate_expired_challenger_model(),
        active_model_deployment := get_active_model_deployment(),
        has_active_model_deployment(active_model_deployment),
        [
            sequence(
                drift_result := drift_check(active_model_deployment),
                has_drift(drift_result),
                [
                    dispatch_training_approval(
                        task_id=DispatchTrainingApprovalTaskIDs.drifted,
                        drift_result=drift_result,
                    ),

                    no_action(task_id=NoActionTaskIDs.no_drift)
                ]
            ),

            dispatch_training_approval(task_id=DispatchTrainingApprovalTaskIDs.cold_start)
        ],
    )

check_training_need()