import sys
import tasks
from tasks import task_generator, LowCriticalityTask
import csv
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


def main(config_file, mode):
    config_name = config_file.split('/')[-1].split('.')[0]
    config = tasks.ProjectConfig(config_file)
    generated_tasks = task_generator.generate_tasks(config)
    cores = [tasks.Processor(f'CPU_{i}', config.core_utilization) for i in range(config.num_of_cores)]

    # worst_fit_decreasing(cores, generated_tasks)
    # show_core_assignments(cores)

    if mode == 'debug':
        show_tasks(generated_tasks)
        print("====================")
        # show_core_assignments(cores)
    elif mode == 'report':
        with open(f'reports/{config_name}-tasks-report.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Task Name', 'Period', 'Criticality', 'WCET-HI', 'WCET-LO', 'Utilization'])
            for t in generated_tasks:
                if isinstance(t, LowCriticalityTask):
                    writer.writerow([t.name, t.period, 'LC', t.wcet, None, t.utilization])
                elif isinstance(t, tasks.HighCriticalityTask):
                    writer.writerow([t.name, t.period, 'HC', t.wcet, t.wcet_lo, t.utilization])
        with open(f'reports/{config_name}-assignment-report.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Task Name', 'Period', 'WCET', 'Utilization', 'Core Name'])
            for c in cores:
                for t in c.tasks:
                    writer.writerow([t.name, t.period, t.wcet, t.utilization, c.name])


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
