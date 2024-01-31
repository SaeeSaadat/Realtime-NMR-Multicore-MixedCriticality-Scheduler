"""
This module is used to generate and define tasks related to the project.
"""

import random
from typing import List

import yaml

from logs import event_logger
from tasks.exceptions import HighCriticalityTaskFailureException
from tasks.exceptions import DuplicateTaskAssignmentException


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
        self.config_name = config_file.split('/')[-1].split('.')[0] + '-' + self.assignment_policy

        if cf.get('random_seed'):
            random.seed(cf['random_seed'])


class Task:
    number_of_tasks = 0

    def __init__(self, period, wcet, utilization, name=None):
        self.period = period
        self.wcet = round(wcet) if round(wcet) >= 1 else 1
        self.utilization = utilization
        self.name = name if name is not None else f'T{Task.number_of_tasks + 1}'
        self.core = None
        if not isinstance(self, HighCriticalityTaskCopy):
            Task.number_of_tasks += 1

    @staticmethod
    def reset_tasks():
        Task.number_of_tasks = 0

    def start(self, time):
        event_logger.log(time, f'[{self.get_core_name()}] Task {self.name} -> START')

    def finish(self, time):
        event_logger.log(time, f'[{self.get_core_name()}] Task {self.name} -> FINISH')

    def fail(self, time):
        event_logger.log(time, f'[{self.get_core_name()}] Task {self.name} -> MISSED DEADLINE!')

    def assign_to_core(self, core):
        self.core = core

    def get_core_name(self):
        if self.core is not None:
            return self.core.name
        return ''


class LowCriticalityTask(Task):
    def __init__(self, period, wcet, utilization, name=None):
        super().__init__(period, wcet, utilization, name)
        self.name = self.name + '-LC'


class HighCriticalityTask(Task):
    def __init__(self, period, wcet_hi, wcet_lo, utilization, number_of_copies=1, name=None):
        super().__init__(period, wcet_hi, utilization, name)
        self.wcet_lo = wcet_lo
        self.name = self.name + '-HC'
        self.number_of_copies = number_of_copies

    def fail(self, time):
        super().fail(time)
        raise HighCriticalityTaskFailureException()


class HighCriticalityTaskCopy(HighCriticalityTask):
    def __init__(self, task: HighCriticalityTask, copy_number=None):
        task_name = task.name.split('-')[0] + f'-Copy{copy_number}' if copy_number is not None else task.name + '-Copy'
        super().__init__(task.period, task.wcet, task.wcet_lo, task.utilization, task.number_of_copies, task_name)
        self.original_task = task

    def cancel(self, time):
        event_logger.log(time, f'Task {self.name} -> CANCEL')


class Processor:
    def __init__(self, name, max_utilization):
        self.name = name
        self.max_utilization = max_utilization
        self.tasks: List[Task] = []

        self.is_failed = False
        self.is_overrun = False

    def add_task(self, task: Task):
        if isinstance(task, HighCriticalityTask):
            if isinstance(task, HighCriticalityTaskCopy):
                if any(filter(
                        lambda t: isinstance(t, HighCriticalityTaskCopy) and t.original_task == task.original_task,
                        self.tasks)):
                    raise DuplicateTaskAssignmentException()
            elif isinstance(task, HighCriticalityTask):
                if any(filter(
                        lambda t: isinstance(t, HighCriticalityTaskCopy) and t.original_task == task,
                        self.tasks)):
                    raise DuplicateTaskAssignmentException()
        self.tasks.append(task)
        task.assign_to_core(self)

    def utilization(self):
        return sum(t.utilization for t in self.tasks)

    def fail(self, time):
        self.is_failed = True
        event_logger.log(time, f'{self.name} -> CORE FAILURE')

    def overrun(self, time):
        self.is_overrun = True
        event_logger.log(time, f'{self.name} -> CORE OVERRUN')

    def calculate_edf_vd_constant(self):
        utilization_hi_lo = sum(t.wcet_lo / t.period for t in self.tasks if isinstance(t, HighCriticalityTask))
        print("\t", utilization_hi_lo)
        utilization_lo_lo = sum(t.wcet / t.period for t in self.tasks if isinstance(t, LowCriticalityTask))
        print("\t", utilization_lo_lo)
        x = utilization_hi_lo / (1 - utilization_lo_lo)
        return x
