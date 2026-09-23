from typing import Annotated, Any

from pydantic import BaseModel, StrictBool, StrictStr, Strict, model_validator, ModelWrapValidatorHandler

from dags.model_lifecycle_orchestrator.check_training_need.modules.configs.airflow.xcom import DriftCheckXComKeys

class DriftCheckResult(BaseModel):
    drift_detected: StrictBool
    drift_summary: Annotated[dict[StrictStr, Annotated[dict, Strict()]], Strict()]

    @model_validator(mode="wrap")
    @classmethod
    def parse_xcom(cls, value: Any, handler: ModelWrapValidatorHandler) -> "DriftCheckResult":
        from dags.shared.modules.schemas.airflow import TaskContext
        if isinstance(value, TaskContext):
            from dags.model_lifecycle_orchestrator.check_training_need.services.tasks import drift_check_operator
            context = value
            task_instance = context.task_instance
            task_id = context.resolve_task_id(drift_check_operator.__name__)
            return cls(
                drift_detected=task_instance.xcom_pull(
                    task_ids=task_id,
                    key=DriftCheckXComKeys.drift_detected,
                ),
                drift_summary=task_instance.xcom_pull(
                    task_ids=task_id,
                    key=DriftCheckXComKeys.drift_summary
                ),
            )
        else:
            return handler(value)