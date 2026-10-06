from datetime import datetime, timezone

from fraud_detection_platform_shim.repositories.mwaa.mwaa import get_mwaa_client

def trigger_airflow_dag(
    dag_id: str,
    endpoint_url: str,
    environment_name: str,
    configurations: dict
) -> None:
    mwaa_client = get_mwaa_client(endpoint_url=endpoint_url)
    response = mwaa_client.invoke_rest_api(
        Name=environment_name,
        Path=f"/dags/{dag_id}/dagRuns",
        Method="POST",
        Body={
            "conf": configurations,
            "logical_date": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        },
    )
    status_code = response.get("RestApiStatusCode")
    if not (200 <= status_code < 300):
        raise RuntimeError(
            f"Unexpected status code {status_code} triggering DAG '{dag_id}'. "
            f"Response: {response.get('RestApiResponse')}"
        )