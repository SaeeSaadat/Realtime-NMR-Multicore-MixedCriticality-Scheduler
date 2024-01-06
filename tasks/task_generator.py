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

    tasks: list[Task] = []
    for u in utilizations[:int(config.num_of_tasks * config.ratio)]:
        # HC Tasks
        period = random.choice(config.periods)
        wcet_hi = u * period
        mu = random.uniform(config.mu_range[0], config.mu_range[1])
        wcet_lo = wcet_hi * mu
        tasks.append(HighCriticalityTask(u, period, wcet_hi, wcet_lo))
        # tasks.append(HighCriticalityTask(u, config.period_range, config.deadline_range, config.wcet_range))



