from typing import Sequence

from airflow.sdk import TaskGroup, BaseOperator
# noinspection protected-member
from airflow.sdk.definitions._internal.contextmanager import TaskGroupContext
from airflow.sdk.definitions.xcom_arg import PlainXComArg

def get_node_entry(node: BaseOperator | TaskGroup | PlainXComArg | Sequence[BaseOperator | TaskGroup | PlainXComArg]):
    if isinstance(node, PlainXComArg):
        task = node.operator
        group = task.task_group
        current_group = TaskGroupContext.get_current(dag=task.get_dag())

        if group is None or current_group is None:
            return task

        while group is not None:
            group_id = group.group_id
            if (
                group_id is not None
                and (child := current_group.children.get(group_id)) is not None
            ):
                return child
            group = group.parent_group

        return task
    else:
        return node

def sequence(*nodes):
    assert nodes
    for i in range(len(nodes) - 1):
        # noinspection statement-effect
        nodes[i] >> nodes[i + 1]
    # To return the first entry in the sequence as a direct downstream
    return get_node_entry(nodes[0])