from typing import cast

from airflow.sdk import Context
# noinspection protected-member
from airflow.sdk.types import DagRunProtocol, RuntimeTaskInstanceProtocol

from dags.shared.modules.schemas.airflow import TaskDAGRun, TaskContext

class TestTaskDAGRun:
    @staticmethod
    def make_dag_run() -> DagRunProtocol:
        return cast(
            DagRunProtocol,
            cast(object, {
                "conf": {}
            })
        )

    def test_instance(self):
        dag_run = self.make_dag_run()
        task_dag_run = TaskDAGRun(dag_run)

        assert task_dag_run.conf == dag_run.conf

class TestTaskContext:
    @staticmethod
    def make_task_instance(**overrides) -> RuntimeTaskInstanceProtocol:
        task_instance = {
            "task_id": "group.current_task"
        }
        task_instance.update(**overrides)
        return cast(
            RuntimeTaskInstanceProtocol,
            cast(object, task_instance)
        )

    def make_context(self, **overrides) -> Context:
        context = {
            "task_instance": self.make_task_instance(),
            "dag_run": TestTaskDAGRun.make_dag_run(),
            "exception": "value",
        }
        context.update(**overrides)
        return cast(
            Context,
            cast(object, context)
        )

    def test_instance(self):
        context = self.make_context()
        task_context = TaskContext(context)

        assert task_context.task_instance == context["task_instance"]
        assert task_context.dag_run == TaskDAGRun(context["dag_run"])
        assert task_context.exception == context["exception"]

    def test_resolve_task_id(self):
        group = "group"
        task_ids = {
            "root": "task_id",
            "group": f"{group}.task_id",
            "nested": f"{group}.{group}.task_id"
        }
        task_contexts = {
            type_of_task_id: TaskContext(self.make_context(
                task_instance=self.make_task_instance(
                    task_id=task_id
                )
            ))
            for type_of_task_id, task_id in task_ids.items()
        }

        task_destination = "destination"
        for type_of_task_id, task_context in task_contexts.items():
            expected = task_context.resolve_task_id(task_destination)

            actual = None
            match type_of_task_id:
                case "root": actual = task_destination
                case "group": actual = f"{group}.{task_destination}"
                case "nested": actual = f"{group}.{group}.{task_destination}"

            assert actual is not None
            assert expected == actual