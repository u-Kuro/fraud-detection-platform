from unittest.mock import patch

# noinspection unused-imports
import tests.services.shared.conftest

patch("drift_check.repositories.postgres.postgres.sql_session.begin").start()