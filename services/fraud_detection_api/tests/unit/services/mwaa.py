import pytest
from pytest_mock import MockerFixture

class TestTriggerAirflowDAG:
    @staticmethod
    def mock_mwaa_client_invoke_rest_api(mocker: MockerFixture, status_code: int):
        mocker.patch(
            target="services.fraud_detection_api.src.repositories.mwaa.mwaa.mwaa_client.invoke_rest_api",
            return_value={"RestApiStatusCode": status_code, "RestApiResponse": {}}
        )

    def test_successful_request(self, mocker: MockerFixture):
        self.mock_mwaa_client_invoke_rest_api(mocker=mocker, status_code=200)

        from services.fraud_detection_api.src.services.mwaa import trigger_airflow_dag

        trigger_airflow_dag(dag_id="id", configurations={})

    def test_bad_request(self, mocker: MockerFixture):
        self.mock_mwaa_client_invoke_rest_api(mocker=mocker, status_code=400)

        from services.fraud_detection_api.src.services.mwaa import trigger_airflow_dag

        with pytest.raises(RuntimeError):
            trigger_airflow_dag(dag_id="id", configurations={})