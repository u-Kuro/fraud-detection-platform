from datetime import datetime
from typing import Any

from airflow.sdk.serde import allow_class
from pydantic import BaseModel, StrictStr, StrictInt, StrictFloat, model_validator, ModelWrapValidatorHandler

class TrainModelResult(BaseModel):
    model_trained_at_datetime: datetime
    model_mlflow_run_id: StrictStr
    model_name: StrictStr
    model_version: StrictInt
    model_dataset_min_datetime: datetime
    model_dataset_max_datetime: datetime
    model_f1_score: StrictFloat
    model_pr_auc: StrictFloat
    model_recall: StrictFloat
    model_precision: StrictFloat

    @model_validator(mode="wrap")
    @classmethod
    def parse_xcom(cls, value: Any, handler: ModelWrapValidatorHandler) -> "TrainModelResult":
        from dags.shared.modules.schemas.airflow import TaskContext

        if isinstance(value, TaskContext):
            from dags.model_lifecycle_orchestrator.on_training_decision.services.tasks import train_model_operator

            task_id = value.resolve_task_id(train_model_operator.__name__)
            payload = value.task_instance.xcom_pull(task_ids=task_id)

            return handler(payload)
        else:
            return handler(value)

allow_class(TrainModelResult)