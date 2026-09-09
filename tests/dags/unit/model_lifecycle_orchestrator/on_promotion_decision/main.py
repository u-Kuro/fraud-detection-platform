from airflow.dag_processing.dagbag import DagBag

class TestOnPromotionDecision:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.dags["on_promotion_decision"]

        assert dag is not None

        assert dag.schedule is None
        assert dag.start_date is None

        assert dag.max_active_runs == 1