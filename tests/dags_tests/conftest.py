from unittest.mock import patch
from uuid import uuid4

import pytest
from airflow.dag_processing.dagbag import DagBag

from dags_shared.modules.configs.project import ProjectConfig

# Postgres
patch("airflow.providers.postgres.hooks.postgres.PostgresHook").start()
patch(
    target="dags_shared.repositories.postgres.projects.get_project_id",
    return_value=uuid4()
).start()

# Slack
patch(target="airflow.providers.slack.hooks.slack.SlackHook").start()

@pytest.fixture(scope="session")
def dag_bag():
    return DagBag(dag_folder=ProjectConfig.dags_path)
