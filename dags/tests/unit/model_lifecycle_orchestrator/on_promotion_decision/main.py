from airflow.dag_processing.dagbag import DagBag

from dags.shared.modules.configs.airflow.dag_ids import DAGIDs

class TestOnPromotionDecision:
    def test_dag(self, dag_bag: DagBag):
        dag = dag_bag.dags[DAGIDs.on_promotion_decision]

        assert dag is not None

        assert dag.schedule is None
        assert dag.start_date is None

        assert dag.max_active_runs == 1