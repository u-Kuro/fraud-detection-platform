from datetime import datetime

from airflow.dag_processing.dagbag import DagBag

from dags.model_lifecycle_orchestrator import check_training_need

class TestCheckTrainingNeed:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.get_dag(check_training_need.__name__)

        assert dag is not None

        assert dag.schedule == "@daily"
        assert isinstance(dag.start_date, datetime)

        assert dag.max_active_runs == 1