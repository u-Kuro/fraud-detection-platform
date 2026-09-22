from unittest.mock import patch

# noinspection unused-imports
import services_shared.tests.conftest

patch("train_model.src.repositories.postgres.postgres.sql_session.begin").start()