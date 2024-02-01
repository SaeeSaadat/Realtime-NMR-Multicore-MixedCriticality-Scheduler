import tasks
from typing import List, Tuple, Dict


class ExecutionSnapshot:
    def __init__(self, time, executed: List[Tuple[tasks.Processor, tasks.TaskInstance]]):
        self.time = time
        self.executed = executed

    def __str__(self):
        return f'Snapshot {self.time}'


class ExecutionTable:
    def __init__(self, cores):
        self.cores = cores
        self.table: Dict[int, ExecutionSnapshot] = {}

    def record_snapshot(self, time, task_instance: tasks.TaskInstance):
        if time not in self.table:
            self.table[time] = ExecutionSnapshot(time, [])
        self.table[time].executed.append((task_instance.task.core, task_instance))

