from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

from dags.model_lifecycle_orchestrator.cold_start.modules.configs.airflow.task_ids import NoActionTaskIDs
from dags.model_lifecycle_orchestrator.cold_start.services.tasks import no_action, seed_transaction_inferences_pod, trigger_check_training_need

def test_no_action():
    task_id = NoActionTaskIDs.has_transaction_inferences
    empty_operator = no_action(task_id=task_id)

    assert isinstance(empty_operator, EmptyOperator)
    assert empty_operator.task_id == task_id

def test_seed_transaction_inferences_pod():
    k8s_operator = seed_transaction_inferences_pod(transaction_inferences_seed_s3_key="value")

    assert isinstance(k8s_operator, KubernetesPodOperator)
    assert k8s_operator.task_id == seed_transaction_inferences_pod.__name__


def test_trigger_check_training_need():
    trigger_dag_run_operator = trigger_check_training_need()

    assert isinstance(trigger_dag_run_operator, TriggerDagRunOperator)
    assert trigger_dag_run_operator.task_id == trigger_check_training_need.__name__