import pytest

from dags_shared.modules.utilities.airflow.airflow import sequence

from unittest.mock import MagicMock

class TestSequence:
    @staticmethod
    @pytest.fixture
    def tasks() -> tuple[MagicMock, ...]:
        return MagicMock(), MagicMock(), MagicMock()

    def test_right_shift(self, tasks: tuple[MagicMock, ...]):
        sequence(*tasks)

        for i in range(len(tasks) - 1):
            tasks[i].__rshift__.assert_called_once_with(tasks[i + 1])

    def test_return(self, tasks: tuple[MagicMock, ...]):
        return_value = sequence(*tasks)

        assert return_value == tasks[0]