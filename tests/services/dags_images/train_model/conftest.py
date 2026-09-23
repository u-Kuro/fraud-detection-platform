from unittest.mock import patch

# noinspection unused-imports
import tests.services.shared.conftest

patch("train_model.repositories.postgres.postgres.sql_session.begin").start()