from unittest.mock import patch
from uuid import uuid4

import pytest
from airflow.dag_processing.dagbag import DagBag

from dags.shared.modules.configs.project import ProjectConfig

# MLflow
# patch(target="mlflow.set_experiment").start()
# patch(target="mlflow.pyfunc.load_model").start()
# patch(target="mlflow.log_artifact").start()
# patch(target="mlflow.log_figure").start()

# Postgres
patch("airflow.providers.postgres.hooks.postgres.PostgresHook").start()
# patch("dags.shared.repositories.postgres.postgres.sql_session.begin").start()
patch(
    target="dags.shared.repositories.postgres.projects.get_project_id",
    return_value=uuid4()
).start()

# S3
# patch(target="boto3.s3.inject.upload_fileobj").start()

# Slack
patch(target="airflow.providers.slack.hooks.slack.SlackHook").start()

@pytest.fixture(scope="session")
def dag_bag():
    return DagBag(dag_folder=ProjectConfig.dags_path)
