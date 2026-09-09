from datetime import datetime

from airflow.dag_processing.dagbag import DagBag

class TestCheckTrainingNeed:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.dags["check_training_need"]

        assert dag is not None

        assert dag.schedule == "@daily"
        assert isinstance(dag.start_date, datetime)

        assert dag.max_active_runs == 1