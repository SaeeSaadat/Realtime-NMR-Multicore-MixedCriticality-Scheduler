"""
This module is used to generate and define tasks related to the project.
"""

from enum import Enum
import yaml


class ProjectConfig:
    """
    This class is used to store the project configuration.
    """

    def __init__(self, config_file: str):
        with open(config_file) as f:
            cf = yaml.load(f, Loader=yaml.FullLoader)

        self.num_of_tasks = cf['num_of_tasks']
        self.ratio = cf['ratio']
        self.core_utilization = cf['core_utilization']
        self.num_of_cores = cf['num_of_cores']
        self.periods = cf['periods']
        self.mu_range = cf['mu_range']
        self.overrun_percentage = cf['overrun_percentage']
        self.error_rate = cf['error_rate']
        self.reliability = cf['reliability']
        self.assignment_policy = cf['assignment_policy']
        self.scheduling_policy = cf['scheduling_policy']


class TaskCriticality(Enum):
    # Maybe not needed
    HC = 1
    LC = 2


class Task:
    pass


class LowCriticalityTask(Task):
    pass


class HighCriticalityTask(Task):
    pass
