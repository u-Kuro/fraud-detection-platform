from datetime import datetime

from airflow.dag_processing.dagbag import DagBag

from dags.shared.modules.configs.airflow.dag_ids import DAGIDs
from dags.shared.services.slack import slack_failure_alert

class TestCheckTrainingNeed:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.dags[DAGIDs.check_training_need]

        assert dag is not None

        assert dag.schedule == "@daily"
        assert isinstance(dag.start_date, datetime)

        assert dag.max_active_runs == 1

        assert dag["on_failure_callback"] is slack_failure_alert

        assert dag.is_paused_upon_creation is False