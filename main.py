import sys
import tasks
from tasks import task_generator, LowCriticalityTask
from pprint import pprint


def main(config_file):
    config = tasks.ProjectConfig(config_file)
    generated_tasks = task_generator.generate_tasks(config)
    for t in generated_tasks:
        if isinstance(t, LowCriticalityTask):
            print(t.name, t.period, t.wcet, t.utilization)
        else:
            print(t.name, t.period, t.wcet, t.wcet_lo, t.utilization, t.number_of_copies)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py {CONFIG_FILE}')
        exit(1)
    main(sys.argv[1])
