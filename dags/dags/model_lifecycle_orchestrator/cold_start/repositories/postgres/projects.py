from airflow.sdk import task
from sqlalchemy.dialects.postgresql import insert

from dags.shared.modules.configs.project import ProjectConfig
from dags.shared.modules.schemas.postgres.projects import Projects
from dags.shared.repositories.postgres.postgres import sql_session

@task
def upsert_project():
    with sql_session.begin() as session:
        session.execute(
            insert(Projects)
            .values(name=ProjectConfig.project_name)
            .on_conflict_do_nothing()
        )