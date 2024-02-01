import sys

import tasks
from tasks import task_generator, LowCriticalityTask
from tasks.exceptions import UnassignableTaskSet
from task_assigner import worst_fit_decreasing, first_fit_decreasing
from reporter import report


def show_tasks(generated_tasks):
    for t in generated_tasks:
        if isinstance(t, LowCriticalityTask):
            print(t.name, t.period, t.wcet, t.utilization)
        else:
            print(t.name, t.period, t.wcet, t.wcet_lo, t.utilization, t.number_of_copies)


def show_core_assignments(cores):
    for c in cores:
        print(c.name, "\tUtilization:", c.utilization())
        for t in c.tasks:
            print('\t', t.name, t.period, t.wcet, t.utilization)


def generate(config_file, mode=None):
    config = tasks.ProjectConfig(config_file)
    generated_tasks = task_generator.generate_tasks(config)
    cores = [tasks.Processor(f'CPU_{i}', config.core_utilization) for i in range(config.num_of_cores)]

    if config.assignment_policy == 'WFD':
        worst_fit_decreasing(cores, generated_tasks)
    elif config.assignment_policy == 'FFD':
        first_fit_decreasing(cores, generated_tasks)
    else:
        raise Exception('Unknown assignment policy: ' + config.assignment_policy)

    if mode == 'debug':
        show_tasks(generated_tasks)
        print("\n====================\n")
        show_core_assignments(cores)
        print("\n====================\n")
        print("Total Utilization:", sum([c.utilization() for c in cores]))

    elif mode == 'report':
        report(config, cores, generated_tasks)
    return cores, generated_tasks


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: python generate.py {CONFIG_FILE} {debug/report}')
        exit(1)
    the_mode = None
    if len(sys.argv) > 2:
        the_mode = sys.argv[2]
        if the_mode not in ['debug', 'report']:
            print('Usage: python generate.py {CONFIG_FILE} {debug/report}')
            exit(1)
    for i in range(1000):
        try:
            generate(sys.argv[1], the_mode)
            print(i, "th try!")
            break
        except UnassignableTaskSet:
            continue
