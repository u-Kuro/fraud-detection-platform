from airflow.dag_processing.dagbag import DagBag

class TestDags:
    def test_import_errors(self, dag_bag: DagBag):
        assert len(dag_bag.import_errors) == 0

    def test_cycles(self, dag_bag: DagBag):
        for dag in dag_bag.dags.values():
            dag.check_cycle()
            assert isinstance(dag.default_args, dict)
            assert callable(dag.default_args.get("on_failure_callback"))
            assert dag.is_paused_upon_creation == False