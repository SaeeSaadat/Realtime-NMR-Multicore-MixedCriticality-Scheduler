import sys
import tasks
from tasks import task_generator, LowCriticalityTask
from task_assigner import worst_fit_decreasing


def show_tasks(generated_tasks):
    for t in generated_tasks:
        if isinstance(t, LowCriticalityTask):
            print(t.name, t.period, t.wcet, t.utilization)
        else:
            print(t.name, t.period, t.wcet, t.wcet_lo, t.utilization, t.number_of_copies)


def show_core_assignments(cores):
    for c in cores:
        print(c.name, c.utilization(), c.max_utilization)
        for t in c.tasks:
            print('\t', t.name, t.period, t.wcet, t.utilization)


def main(config_file, debug=False):
    config = tasks.ProjectConfig(config_file)
    generated_tasks = task_generator.generate_tasks(config)
    cores = [tasks.Processor(f'CPU_{i}', config.core_utilization) for i in range(config.num_of_cores)]

    # worst_fit_decreasing(cores, generated_tasks)
    # show_core_assignments(cores)

    if debug:
        show_tasks(generated_tasks)
        print("====================")
        # show_core_assignments(cores)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py {CONFIG_FILE}')
        exit(1)
    should_debug = len(sys.argv) > 2 and sys.argv[2] == 'debug'
    main(sys.argv[1], should_debug)
