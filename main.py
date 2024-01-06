import os
import sys
import tasks
from pprint import pprint


def main(config_file):
    config = tasks.ProjectConfig(config_file)
    pprint(config.reliability)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('Usage: python main.py {CONFIG_FILE}')
        exit(1)
    main(sys.argv[1])
