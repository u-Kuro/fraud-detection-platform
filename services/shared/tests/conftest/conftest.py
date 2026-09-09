from unittest.mock import patch
from uuid import uuid4

# Import stage
patch("services.shared.src.repositories.postgres.projects.get_project_id", return_value=uuid4()).start()
patch("boto3.s3.inject.upload_fileobj").start()
patch("mlflow.set_experiment").start()