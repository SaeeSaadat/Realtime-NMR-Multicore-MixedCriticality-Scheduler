import sys
import tasks
from tasks import task_generator
from pprint import pprint


def main(config_file):
    config = tasks.ProjectConfig(config_file)
    generated_tasks = task_generator.generate_tasks(config)
    print(generated_tasks)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('Usage: python main.py {CONFIG_FILE}')
        exit(1)
    main(sys.argv[1])
