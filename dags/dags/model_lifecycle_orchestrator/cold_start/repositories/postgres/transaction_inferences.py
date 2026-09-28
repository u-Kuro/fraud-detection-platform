from airflow.sdk import task, get_current_context
from sqlalchemy import select, func

from dags.model_lifecycle_orchestrator.cold_start.modules.configs.airflow.task_ids import NoActionTaskIDs
from dags.model_lifecycle_orchestrator.cold_start.services.tasks import get_transaction_inferences_seed
from dags.shared.modules.schemas.airflow import TaskContext
from dags.shared.modules.schemas.postgres.transaction_inferences import TransactionInferences
from dags.shared.repositories.postgres.postgres import sql_session

@task.branch
def is_transaction_inferences_empty() -> str:
    context = TaskContext(get_current_context())

    with sql_session.begin() as session:
        count = session.execute(
            select(func.count())
            .select_from(TransactionInferences)
        ).scalar_one()

    if count == 0:
        return context.resolve_task_id(
            task_id=get_transaction_inferences_seed.function.__name__
        )
    else:
        return context.resolve_task_id(
            task_id=NoActionTaskIDs.has_transaction_inferences
        )