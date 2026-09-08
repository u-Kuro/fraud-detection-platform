import pytest

from pytest_mock import MockerFixture

@pytest.fixture(
    autouse=True,
    scope="session"
)
def mock_boto3(mocker: MockerFixture):
    pass
    # mocker.patch(target="boto3")

@pytest.fixture(
    autouse=True,
    scope="session"
)
def mock_mlflow(mocker: MockerFixture):
    pass
    # mocker.patch(target="mlflow")

@pytest.fixture(
    autouse=True,
    scope="session"
)
def mock_slack_bolt(mocker: MockerFixture):
    pass
    # mocker.patch(target="slack_bolt")
    # mocker.patch(target="slack_bolt.App")

@pytest.fixture(
    autouse=True,
    scope="session"
)
def mock_sqlalchemy(mocker: MockerFixture):
    pass
    # mocker.patch(target="sqlalchemy")
    # mocker.patch(target="sqlalchemy.orm.sessionmaker")



