import sys

import tasks
from tasks import task_generator, LowCriticalityTask
from task_assigner import worst_fit_decreasing
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


def main(config_file, mode):
    config_name = config_file.split('/')[-1].split('.')[0]
    config = tasks.ProjectConfig(config_file)
    generated_tasks = task_generator.generate_tasks(config)
    cores = [tasks.Processor(f'CPU_{i}', config.core_utilization) for i in range(config.num_of_cores)]

    worst_fit_decreasing(cores, generated_tasks)

    if mode == 'debug':
        show_tasks(generated_tasks)
        print("\n====================\n")
        show_core_assignments(cores)
        print("\n====================\n")
        print("Total Utilization:", sum([c.utilization() for c in cores]))

    elif mode == 'report':
        report(config, cores, generated_tasks)



if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: python main.py {CONFIG_FILE} {debug/report}')
        exit(1)
    if len(sys.argv) > 2:
        the_mode = sys.argv[2]
        if the_mode not in ['debug', 'report']:
            print('Usage: python main.py {CONFIG_FILE} {debug/report}')
            exit(1)
        main(sys.argv[1], the_mode)
