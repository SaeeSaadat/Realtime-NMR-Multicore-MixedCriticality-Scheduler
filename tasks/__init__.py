"""
This module is used to generate and define tasks related to the project.
"""

import random
from typing import List, Optional

import yaml

from logs import event_logger
from tasks.exceptions import HighCriticalityTaskFailureException
from tasks.exceptions import DuplicateTaskAssignmentException
from tasks.exceptions import LowCriticalityJobWhileOverrun


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
        self.core: Optional[Processor] = None
        self.instances = []
        self.is_active = True
        if not isinstance(self, HighCriticalityTaskCopy):
            Task.number_of_tasks += 1

    def duration(self):
        return self.wcet

    @staticmethod
    def reset_tasks():
        Task.number_of_tasks = 0

    def assign_to_core(self, core):
        self.core = core

    def get_core_name(self):
        if self.core is not None:
            return self.core.name
        return ''

    def missed_deadline(self, time, job):
        pass

    def instantiate(self, time: int, deadline: int = None) -> 'TaskInstance':
        instance = TaskInstance(self, time, deadline=deadline)
        self.instances.append(instance)
        return instance

    @property
    def is_actual_deadline_same_as_period(self):
        """
        HC tasks in EDF-VD will have a deadline different from their period
        If the time is past their virtual deadline but not their actual periodical deadline, are they considered failed?
        If this function returns True, then they are considered failed only AFTER they go past their PERIOD!
        """
        return True


class TaskInstance:
    def __init__(self, task: Task, release_time: int, duration: int = None, deadline: int = None):
        self.task = task
        self.release_time = release_time
        self.deadline = deadline if deadline is not None else release_time + self.task.period
        self.start_time = None
        self.end_time = None
        self.duration = duration if duration is not None else self.task.duration()
        self.remaining_time = self.duration
        self.number = len(task.instances) + 1
        self.deadline_missed_time = None
        self.overrun_time = None
        self.is_failed = False
        event_logger.log(
            release_time,
            f'[{self.task.get_core_name()}] Task {self.task.name}::'
            f'{self.number} -> RELEASE, Deadline: {self.deadline}'
        )

    def __eq__(self, other):
        return self.task == other.task and self.number == other.number

    def execute(self, time: int):
        if self.start_time is None:
            event_logger.log(time, f'[{self.task.get_core_name()}] Task {self.task.name} -> START')
            self.start_time = time
        self.remaining_time -= 1
        self.end_time = time + 1
        if self.task.core.is_failed:
            self.is_failed = True

    def __repr__(self):
        return f'{self.task.name}::{self.number}'

    def finish(self, time):
        event_logger.log(time, f'[{self.task.get_core_name()}] Task {self.task.name} -> FINISH')

    def is_past_deadline(self, time) -> bool:
        if time < self.deadline or self.remaining_time <= 0:
            return False
        if self.task.is_actual_deadline_same_as_period:
            return time > self.release_time + self.task.period
        return True

    def miss_deadline(self, time):
        if not self.is_past_deadline(time):
            raise Exception(f"Task {self} is not failed!")
        self.deadline_missed_time = time
        print(f"Task {self} missed deadline at {time}")
        self.task.missed_deadline(time, self)
        event_logger.log(time,
                         f'[{self.task.get_core_name()}] Task {self.task.name}::{self.number} -> MISSED DEADLINE!')

    @property
    def is_finished(self):
        return self.remaining_time <= 0

    def has_missed_deadline(self, current_time: int):
        return not self.is_finished and current_time > self.deadline


class LowCriticalityTask(Task):
    def __init__(self, period, wcet, utilization, name=None):
        super().__init__(period, wcet, utilization, name)
        self.name = self.name + '-LC'
        self.quality_time = 0
        self.total_time = 0

    def instantiate(self, time: int, deadline: int = None) -> 'TaskInstance':
        if self.core.is_overrun:
            raise LowCriticalityJobWhileOverrun()
        instance = super().instantiate(time, deadline)
        instance.duration = self.wcet
        return instance

class HighCriticalityTask(Task):
    def __init__(self, period, wcet_hi, wcet_lo, utilization, number_of_copies=1, name=None):
        super().__init__(period, wcet_hi, utilization, name)
        self.wcet_hi = wcet_hi
        self.wcet_lo = wcet_lo
        self.name = self.name + '-HC'
        self.number_of_copies = number_of_copies

    def duration(self):
        if self.core.is_overrun:
            print("Overrun!")
        return self.wcet_hi if self.core.is_overrun else self.wcet_lo

    def missed_deadline(self, time, job: TaskInstance):
        super().missed_deadline(time, job)
        event_logger.log(time, f'HIGH CRITICALITY TASK {self.name} -> MISSED DEADLINE')
        raise HighCriticalityTaskFailureException(job)


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
        if not any(filter(lambda t: isinstance(t, HighCriticalityTask), self.tasks)):
            return 1
        utilization_hi_lo = sum(t.wcet_lo / t.period for t in self.tasks if isinstance(t, HighCriticalityTask))
        utilization_lo_lo = sum(t.wcet / t.period for t in self.tasks if isinstance(t, LowCriticalityTask))
        x = utilization_hi_lo / (1 - utilization_lo_lo)
        return x
