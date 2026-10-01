import gzip
from unittest.mock import MagicMock

import pytest
from pandas import DataFrame
from pytest_mock import MockerFixture

class GetTransactionInferencesSeedIterator:
    @staticmethod
    @pytest.fixture
    def mocked_download_fileobject(mocker: MockerFixture) -> MagicMock:
        entries = {
            '"Time"': '0',
            '"Amount"': '1.0',
            '"Class"': '"0"',
            **{
                f'"V{i}"': '1.0'
                for i in range(1, 29)
            }
        }

        header = ",".join(entries.keys())
        row = ",".join(entries.values())

        gzipped_csv = gzip.compress(data="\n".join([header] + [row] * 3).encode())

        return mocker.patch(
            target="shared.repositories.s3.s3.s3_client.download_fileobj",
            side_effect=lambda **kwargs: kwargs["Fileobj"].write(gzipped_csv),
        )

    @staticmethod
    def test_get_transaction_inferences_seed_iterator(mocked_download_fileobject: MagicMock):
        from seed_transaction_inferences.repositories.s3.transaction_inferences_seed import get_transaction_inferences_seed_iterator

        for result in get_transaction_inferences_seed_iterator():
            assert isinstance(result, DataFrame)
            assert 3 <= len(result) <= 2_000
            assert "Time" in result.columns
            assert "Amount" in result.columns
            assert "Class" in result.columns
            assert all(f"V{i}" in result.columns for i in range(1, 29))