import tasks
from typing import List, Tuple, Dict


class ExecutionSnapshot:
    def __init__(self, time, executed: List[Tuple[tasks.Processor, tasks.TaskInstance]] = None):
        self.time = time
        self.executed = executed if executed is not None else []

    def add(self, task_instance: tasks.TaskInstance):
        self.executed.append((task_instance.task.core, task_instance))

    def __str__(self):
        return f'Snapshot {self.time}'


class ExecutionTable:
    def __init__(self, hyper_period: int):
        self.table: Dict[int, ExecutionSnapshot] = {i: ExecutionSnapshot(i) for i in range(hyper_period+1)}

    def record_snapshot(self, time, task_instance: tasks.TaskInstance):
        self.table[time].add(task_instance)

