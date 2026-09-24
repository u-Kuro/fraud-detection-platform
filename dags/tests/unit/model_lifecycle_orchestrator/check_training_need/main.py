from datetime import datetime

from airflow.dag_processing.dagbag import DagBag

from dags.shared.modules.configs.airflow.dag_ids import DAGIDs

class TestCheckTrainingNeed:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.dags[DAGIDs.check_training_need]

        assert dag is not None

        assert dag.schedule == "@daily"
        assert isinstance(dag.start_date, datetime)

        assert dag.max_active_runs == 1