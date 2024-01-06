import tasks
from tasks import ProjectConfig
from tasks import uunifast
"""
This file should be visible to other modules
Generating the tasks must be done using this file
"""


def generate_tasks(config: ProjectConfig):
    uunifast.generate_uunifast_discard(config.nsets, config.u, config.n, 'task_utilizations.csv')

