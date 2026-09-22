from datetime import datetime

from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.http.operators.http import HttpOperator

from model_lifecycle_orchestrator.on_promotion_decision.services.tasks import apply_model_deployment, archive_transaction_inferences_used_for_deployed_model

def test_apply_model_deployment():
    http_operator = apply_model_deployment()

    assert isinstance(http_operator, HttpOperator)
    assert http_operator.task_id == apply_model_deployment.__name__

def test_archive_transaction_inferences_used_for_deployed_model():
    k8s_operator = archive_transaction_inferences_used_for_deployed_model(transaction_inferences_iso_datetime_cutoff=datetime.now().isoformat())

    assert isinstance(k8s_operator, KubernetesPodOperator)
    assert k8s_operator.task_id == archive_transaction_inferences_used_for_deployed_model.__name__