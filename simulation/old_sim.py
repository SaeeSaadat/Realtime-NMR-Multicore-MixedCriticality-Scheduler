import math
from typing import List, Dict

from logs import event_logger
from simulation import exceptions, failure_manager

import tasks


def run(
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

    time = 0
    active_tasks: Dict[tasks.Processor, List[tasks.TaskInstance]] = {core: [] for core in cores}

    while time < hyper_period:
        # Check if core has failure or overrun
        if time in core_failures:
            core_failures[time].fail(time)
        if time in core_overruns:
            core_overruns[time].overrun(time)

        for core in cores:
            if not edf_only:
                if core.is_overrun:
                    # drop all LC tasks from active_tasks
                    # move HC deadlines to their Wcet_hi situation!
                    active_tasks[core] = {task: (deadline + (task.wcet - task.wcet_lo), remaining_time) for
                                          task, (deadline, remaining_time) in
                                          active_tasks[core].items() if isinstance(task, tasks.HighCriticalityTask)}

            # Check if any tasks are released
            for task in core.tasks:
                period = task.period
                if not edf_only and isinstance(task, tasks.HighCriticalityTask) and not core.is_overrun:
                    period = period * core.calculate_edf_vd_constant()
                if time % period == 0:
                    wcet = task.wcet
                    if not edf_only and isinstance(task, tasks.HighCriticalityTask) and not core.is_overrun:
                        wcet = task.wcet_lo

                    active_tasks[core][task] = (time + period, wcet)

            # Check if any tasks are finished
            finished_tasks = [task for task, (deadline, remaining_time) in active_tasks[core].items() if
                              remaining_time == 0]
            for task in finished_tasks:
                task.finish(time)
                active_tasks[core].pop(task)

                # If it's a high criticality task, its copies can be dropped
                if isinstance(task, tasks.HighCriticalityTask):
                    task_origin = task.original_task if isinstance(task, tasks.HighCriticalityTaskCopy) else task
                    for task_sets in active_tasks.values():
                        for t in task_sets.keys():
                            if isinstance(t, tasks.HighCriticalityTaskCopy) and t.original_task == task_origin:
                                task_sets.pop(t)
                                t.cancel(time)

            # Check if any deadlines are missed
            missed_deadline_tasks = [task for task, (deadline, remaining_time) in active_tasks[core].items() if
                                     remaining_time > 0 and deadline <= time]
            for task in missed_deadline_tasks:
                task.fail(time)
                # If it's a high criticality task, it will automatically raise an exception
                # remove the task from active_tasks
                active_tasks[core].pop(task)

            # Select the task with the highest priority, using the EDF-VD scheduling policy
            if active_tasks[core]:
                task = min(active_tasks[core].keys(), key=lambda t: active_tasks[core][t][0])
                wcet = task.wcet
                if isinstance(task, tasks.HighCriticalityTask):
                    wcet = task.wcet_lo
                    if not edf_only and core.is_overrun:
                        wcet = task.wcet
                if active_tasks[core][task][1] == wcet:
                    task.start(time)
                active_tasks[core][task] = (active_tasks[core][task][0], active_tasks[core][task][1] - 1)

        time += 1
