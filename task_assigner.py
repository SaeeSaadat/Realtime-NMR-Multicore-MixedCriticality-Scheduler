from tasks import Task, HighCriticalityTask, LowCriticalityTask, ProjectConfig, Processor
from typing import List


def worst_fit_decreasing(cores: List[Processor], tasks: List[Task]):
    tasks = sorted(tasks, key=lambda t: t.utilization, reverse=True)
    for t in tasks:
        for c in cores:
            if 1 - c.utilization() >= t.utilization:
                c.add_task(t)
                break
        else:
            raise Exception('No core found for task ' + t.name)
