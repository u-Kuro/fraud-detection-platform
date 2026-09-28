import gzip

from pandas import DataFrame
from pytest_mock import MockerFixture

def test_get_transaction_inferences_seed_csv(mocker: MockerFixture):
    csv_header = f'"Time",{','.join(f'"V{i}"' for i in range(1, 29))},"Amount","Class"'
    csv_row = f'0,{','.join(['1.0'] * 28)},1.0,"0"'
    gzipped_csv = gzip.compress(data=f"{csv_header}\n{csv_row}".encode())

    mocker.patch(
        target="shared.repositories.s3.s3.s3_client.download_fileobj",
        side_effect=lambda **kwargs: kwargs["Fileobj"].write(gzipped_csv)
    )

    from seed_transaction_inferences.repositories.s3.transaction_inferences_seed import get_transaction_inferences_seed_csv
    result = get_transaction_inferences_seed_csv()

    assert isinstance(result, DataFrame)
    assert len(result) == 1
    assert "Time" in result.columns
    assert "Amount" in result.columns
    assert "Class" in result.columns
    assert all(f"V{i}" in result.columns for i in range(1, 29))