import random
import math

from tasks import Task, HighCriticalityTask, LowCriticalityTask, HighCriticalityTaskCopy
from tasks import ProjectConfig
from tasks import uunifast
from tasks.n_modular_redundancy import calculated_number_of_copies
"""
This file should be visible to other modules
Generating the tasks must be done using this file
"""


def generate_tasks(config: ProjectConfig):
    num_of_copies = calculated_number_of_copies(config.reliability, config.error_rate)
    utilizations = (
        uunifast.generate_uunifast_discard(config.num_of_cores * config.core_utilization, config.num_of_tasks))

    Task.reset_tasks()
    tasks: list[Task] = []
    partition = math.ceil(config.num_of_tasks * config.ratio)
    for u in utilizations[:partition]:
        # HC Tasks
        util = u / num_of_copies
        # Not sure if this is a good idea, but it's the only one I've got!
        period = random.choice(config.periods)
        wcet_hi = util * period
        mu = random.uniform(config.mu_range[0], config.mu_range[1])
        wcet_lo = wcet_hi * mu
        task = HighCriticalityTask(period, wcet_hi, wcet_lo, util, num_of_copies)
        tasks.append(task)
        for i in range(1, num_of_copies):
            tasks.append(HighCriticalityTaskCopy(task, i))

    for u in utilizations[partition:]:
        # LC Tasks
        period = random.choice(config.periods)
        wcet = u * period
        tasks.append(LowCriticalityTask(period, wcet, u))

    return tasks



