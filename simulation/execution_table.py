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
        self.table: Dict[int, ExecutionSnapshot] = {i: ExecutionSnapshot(i) for i in range(hyper_period + 1)}
        self.all_jobs: List[tasks.TaskInstance] = []

    def record_snapshot(self, time, task_instance: tasks.TaskInstance):
        self.table[time].add(task_instance)

    def register_all_jobs(self, jobs: List[tasks.TaskInstance]):
        self.all_jobs = jobs

    @property
    def all_lc_jobs(self):
        return [job for job in self.all_jobs if isinstance(job.task, tasks.LowCriticalityTask)]

    @property
    def all_hc_jobs(self):
        return [job for job in self.all_jobs if isinstance(job.task, tasks.HighCriticalityTask)]

    @property
    def average_qos(self) -> float:
        return sum([job.quality_of_service for job in self.all_lc_jobs]) / len(self.all_lc_jobs)

    @property
    def is_schedulable(self) -> bool:
        return not any([job.deadline_missed_time is not None for job in self.all_hc_jobs])
