from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from model_lifecycle_orchestrator.on_training_decision.services.tasks import train_model_operator

def test_train_model_operator():
    k8s_operator = train_model_operator()

    assert isinstance(k8s_operator, KubernetesPodOperator)
    assert k8s_operator.task_id == train_model_operator.__name__