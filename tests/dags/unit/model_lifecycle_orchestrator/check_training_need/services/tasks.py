from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.standard.operators.empty import EmptyOperator

from dags.model_lifecycle_orchestrator.check_training_need.modules.configs.airflow.task_ids import NoActionTaskIDs
from dags.model_lifecycle_orchestrator.check_training_need.modules.schemas.airflow.tasks import ActiveModelDeployment
from dags.model_lifecycle_orchestrator.check_training_need.services.tasks import no_action, drift_check_operator

def test_no_action():
    task_id = NoActionTaskIDs.no_drift
    empty_operator = no_action(task_id=task_id)

    assert isinstance(empty_operator, EmptyOperator)
    assert empty_operator.task_id == task_id

def test_drift_check_operator():
    k8s_operator = drift_check_operator(active_model_deployment_mlflow_run_id="value")

    assert isinstance(k8s_operator, KubernetesPodOperator)
    assert k8s_operator.task_id == drift_check_operator.__name__
