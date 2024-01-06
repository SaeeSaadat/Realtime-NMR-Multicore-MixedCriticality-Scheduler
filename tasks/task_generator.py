import random

from tasks import Task, HighCriticalityTask, LowCriticalityTask
from tasks import ProjectConfig
from tasks import uunifast
"""
This file should be visible to other modules
Generating the tasks must be done using this file
"""


def generate_tasks(config: ProjectConfig):
    utilizations = (
        uunifast.generate_uunifast_discard(1, config.num_of_cores * config.core_utilization, config.num_of_tasks))[0]

    Task.reset_tasks()
    tasks: list[Task] = []
    partition = int(config.num_of_tasks * config.ratio)
    for u in utilizations[:partition]:
        # HC Tasks
        period = random.choice(config.periods)
        wcet_hi = u * period
        mu = random.uniform(config.mu_range[0], config.mu_range[1])
        wcet_lo = wcet_hi * mu
        tasks.append(HighCriticalityTask(period, wcet_hi, wcet_lo, u))

    for u in utilizations[partition:]:
        # LC Tasks
        period = random.choice(config.periods)
        wcet = u * period
        tasks.append(LowCriticalityTask(period, wcet, u))

    return tasks



