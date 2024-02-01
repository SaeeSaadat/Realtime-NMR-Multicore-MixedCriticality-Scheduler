import math
from typing import List, Dict

from logs import event_logger
from simulation import exceptions, failure_manager

import tasks


def run_simulation(
        cores: List[tasks.Processor],
        overrun_probability=0,
        task_fail_probability=0,
        edf_only=False
):
    hyper_period = math.lcm(
        *(math.lcm(*(t.period for t in core.tasks)) for core in cores)
    )

    core_failures = failure_manager.calculate_failures(cores, task_fail_probability, hyper_period)
    core_overruns = failure_manager.calculate_failures(cores, overrun_probability, hyper_period)

    active_tasks: Dict[tasks.Processor, List[tasks.TaskInstance]] = {core: [] for core in cores}

    for time in range(hyper_period+1):
        # Check if core has failure or overrun
        if time in core_failures:
            core_failures[time].fail(time)
        if time in core_overruns:
            core_overruns[time].overrun(time)
        for core in cores:
            pass

            # Update active tasks
            # Check for finished tasks

            # Check for tasks past their deadlines

            # Check for failed tasks

            # Check for released tasks

            # Sort tasks based on their deadline





