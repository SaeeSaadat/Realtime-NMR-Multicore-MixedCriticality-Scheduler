from tasks import Task, Processor, HighCriticalityTask
from typing import List


def worst_fit_decreasing(cores: List[Processor], tasks: List[Task]):
    tasks = sorted(tasks, key=lambda t: (isinstance(t, HighCriticalityTask), t.utilization), reverse=True)
    for t in tasks:
        cores = sorted(cores, key=lambda c: c.utilization())
        for c in cores:
            if 1 - c.utilization() >= t.utilization:
                c.add_task(t)
                break
        else:
            raise Exception('No core found for task ' + t.name)


def first_fit_decreasing(cores: List[Processor], tasks: List[Task]):
    tasks = sorted(tasks, key=lambda t: (isinstance(t, HighCriticalityTask), t.utilization), reverse=True)
    for t in tasks:
        for c in cores:
            if 1 - c.utilization() >= t.utilization:
                c.add_task(t)
                break
        else:
            raise Exception('No core found for task ' + t.name)
