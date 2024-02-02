import math
from typing import List, Dict

from logs import event_logger
from simulation import exceptions, failure_manager, chart_maker
from simulation.execution_table import ExecutionTable

import tasks


def run_simulation(
        cores: List[tasks.Processor],
        overrun_probability=0,
        task_fail_probability=0,
        edf_only=False,
        should_plot=True
):
    hyper_period = math.lcm(
        *(math.lcm(*(t.period for t in core.tasks)) for core in cores)
    )

    execution_table = ExecutionTable(hyper_period)

    core_failures = failure_manager.calculate_failures(cores, task_fail_probability, hyper_period)
    core_overruns = failure_manager.calculate_failures(cores, overrun_probability, hyper_period)
    overrunning_cores = []

    all_jobs: List[tasks.TaskInstance] = []
    active_jobs: Dict[tasks.Processor, List[tasks.TaskInstance]] = {core: [] for core in cores}

    for time in range(hyper_period + 1):
        # Check if core has failure or overrun
        if time in core_failures:
            core_failures[time].fail(time)
        if time in core_overruns:
            overrunning_cores.append(core_overruns[time])
        for core in cores:

            # Check for finished jobs
            for job in active_jobs[core]:
                if job.is_finished:
                    job.finish(time)
                    active_jobs[core].remove(job)
                    temp = 0

            # Check for jobs past their deadlines
            for job in active_jobs[core]:
                if job.is_failed(time):
                    job.fail(time)
                    active_jobs[core].remove(job)

            # Check for tasks with missed deadline

            # Check for released tasks
            for task in core.tasks:
                if time % task.period == 0:
                    job = task.instantiate(time)
                    all_jobs.append(job)
                    active_jobs[core].append(job)

            # Sort tasks based on their deadline
            active_jobs[core].sort(key=lambda x: x.deadline)

            # select the task with the earliest deadline and execute it
            if len(active_jobs[core]) > 0:
                job = active_jobs[core][0]
                job.execute(time)
                execution_table.record_snapshot(time, job)

            # If it's HC and the core is supposed to overrun, overrun it! (and update the active tasks)

    if should_plot:
        chart_maker.plot_gantt_chart(hyper_period, all_jobs, cores, core_overruns, core_failures)
