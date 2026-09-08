from airflow.dag_processing.dagbag import DagBag

from dags.model_lifecycle_orchestrator import on_training_decision

class TestOnTrainingDecision:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.get_dag(on_training_decision.__name__)

        assert dag is not None

        assert dag.schedule is None
        assert dag.start_date is None

        assert dag.max_active_runs == 1