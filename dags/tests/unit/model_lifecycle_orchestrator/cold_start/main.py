from airflow.dag_processing.dagbag import DagBag

from dags.shared.modules.configs.airflow.dag_ids import DAGIDs
from dags.shared.services.slack import slack_failure_alert

class TestColdStart:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.dags[DAGIDs.cold_start]

        assert dag is not None

        assert dag.schedule is None
        assert dag.start_date is None

        assert dag.max_active_runs == 1

        assert dag.default_args["on_failure_callback"] is slack_failure_alert

        assert dag.is_paused_upon_creation is False