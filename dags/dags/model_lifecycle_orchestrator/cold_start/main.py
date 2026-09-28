from airflow.sdk import dag

from dags.model_lifecycle_orchestrator.cold_start.modules.configs.airflow.task_ids import NoActionTaskIDs
from dags.model_lifecycle_orchestrator.cold_start.repositories.postgres.projects import upsert_project
from dags.model_lifecycle_orchestrator.cold_start.repositories.postgres.transaction_inferences import is_transaction_inferences_empty
from dags.model_lifecycle_orchestrator.cold_start.services.tasks import get_transaction_inferences_seed_s3_key, seed_transaction_inferences_pod, trigger_check_training_need, no_action
from dags.shared.modules.configs.airflow.dag_ids import DAGIDs
from dags.shared.modules.configs.project import ProjectConfig
from dags.shared.modules.utilities.airflow.airflow import sequence
from dags.shared.services.slack import slack_failure_alert

@dag(
    dag_id=DAGIDs.cold_start,
    max_active_runs=1,
    default_args={
        "on_failure_callback": slack_failure_alert
    },
    is_paused_upon_creation=False,
    tags=[ProjectConfig.project_name, "triggered", "cold_start"],
)
def cold_start():
    sequence(
        upsert_project(),
        is_transaction_inferences_empty(),
        [
            sequence(
                transaction_inferences_seed_s3_key := get_transaction_inferences_seed_s3_key(),
                seed_transaction_inferences_pod(
                    transaction_inferences_seed_s3_key=transaction_inferences_seed_s3_key
                ),
                trigger_check_training_need(),
            ),

            no_action(NoActionTaskIDs.has_transaction_inferences),
        ],
    )

cold_start()