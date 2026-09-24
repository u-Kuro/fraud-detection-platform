from unittest.mock import patch
from uuid import uuid4

# MLflow
patch(target="mlflow.set_experiment").start()
patch(target="mlflow.pyfunc.load_model").start()
patch(target="mlflow.log_artifact").start()
patch(target="mlflow.log_figure").start()

# Postgres
patch(
    target="shared.repositories.postgres.projects.get_project_id",
    return_value=uuid4()
).start()

# S3
patch(target="boto3.s3.inject.upload_fileobj").start()