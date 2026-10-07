from typing import Any

from airflow.sdk.serde import allow_class
from pydantic import BaseModel, StrictBool, StrictStr, model_validator, ModelWrapValidatorHandler

class DriftCheckResultValidation(BaseModel):
    has_enough_current_data: StrictBool

    @model_validator(mode="wrap")
    @classmethod
    def parse_xcom(cls, value: Any, handler: ModelWrapValidatorHandler) -> "DriftCheckResultValidation":
        from dags.shared.modules.schemas.airflow import TaskContext

        if isinstance(value, TaskContext):
            from dags.model_lifecycle_orchestrator.check_training_need.services.tasks import drift_check_operator

            task_id = value.resolve_task_id(drift_check_operator.__name__)
            payload = value.task_instance.xcom_pull(task_ids=task_id)

            return handler(payload)
        else:
            return handler(value)

class DriftCheckResult(BaseModel):
    drift_detected: StrictBool
    drift_summary: dict[StrictStr, dict]

    @model_validator(mode="wrap")
    @classmethod
    def parse_xcom(cls, value: Any, handler: ModelWrapValidatorHandler) -> "DriftCheckResult":
        from dags.shared.modules.schemas.airflow import TaskContext

        if isinstance(value, TaskContext):
            from dags.model_lifecycle_orchestrator.check_training_need.services.tasks import drift_check_operator

            task_id = value.resolve_task_id(drift_check_operator.__name__)
            payload = value.task_instance.xcom_pull(task_ids=task_id)

            return handler(payload)
        else:
            return handler(value)

allow_class(DriftCheckResultValidation)
allow_class(DriftCheckResult)