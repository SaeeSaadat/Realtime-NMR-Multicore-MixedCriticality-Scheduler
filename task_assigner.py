from typing import List

from tasks import Task, Processor, HighCriticalityTask
from tasks.exceptions import DuplicateTaskAssignmentException, UnassignableTaskSet


def worst_fit_decreasing(cores: List[Processor], tasks: List[Task]):
    tasks = sorted(tasks, key=lambda t: (isinstance(t, HighCriticalityTask), t.utilization), reverse=True)
    for t in tasks:
        cores = sorted(cores, key=lambda c: c.utilization())
        for c in cores:
            if 1 - c.utilization() >= t.utilization:
                try:
                    c.add_task(t)
                    break
                except DuplicateTaskAssignmentException:
                    continue
        else:
            raise UnassignableTaskSet('No core found for task ' + t.name)


def first_fit_decreasing(cores: List[Processor], tasks: List[Task]):
    tasks = sorted(tasks, key=lambda t: (isinstance(t, HighCriticalityTask), t.utilization), reverse=True)
    for t in tasks:
        for c in cores:
            if 1 - c.utilization() >= t.utilization:
                try:
                    c.add_task(t)
                    break
                except DuplicateTaskAssignmentException:
                    continue
        else:
            raise UnassignableTaskSet('No core found for task ' + t.name)
