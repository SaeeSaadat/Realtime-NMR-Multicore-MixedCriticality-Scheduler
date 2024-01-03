"""
This module is used to generate and define tasks related to the project.
"""

from enum import Enum


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
