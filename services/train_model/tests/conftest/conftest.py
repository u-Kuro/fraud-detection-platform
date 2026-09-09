from unittest.mock import patch

# noinspection unused-imports
import services.shared.tests.conftest.conftest # noqa: F401

patch("services.train_model.src.repositories.postgres.postgres.sql_session.begin").start()