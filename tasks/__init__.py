"""
This module is used to generate and define tasks related to the project.
"""

import random
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

        if cf.get('random_seed'):
            random.seed(cf['random_seed'])


class Task:
    number_of_tasks = 0

    def __init__(self, period, wcet, utilization, name=None):
        self.period = period
        self.wcet = wcet
        self.utilization = utilization
        self.name = name if name is not None else f'T{Task.number_of_tasks + 1}'
        Task.number_of_tasks += 1

    @staticmethod
    def reset_tasks():
        Task.number_of_tasks = 0


class LowCriticalityTask(Task):
    def __init__(self, period, wcet, utilization, name=None):
        super().__init__(period, wcet, utilization, name)
        self.name = self.name + '-LC'


class HighCriticalityTask(Task):
    def __init__(self, period, wcet_hi, wcet_lo, utilization, name=None):
        super().__init__(period, wcet_hi, utilization, name)
        self.wcet_lo = wcet_lo
        self.name = self.name + '-HC'
