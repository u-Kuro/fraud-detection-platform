from unittest.mock import patch

# noinspection unused-imports
import services_shared.tests.conftest

patch("drift_check.src.repositories.postgres.postgres.sql_session.begin").start()