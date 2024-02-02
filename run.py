import os
import sys

import tqdm
import yaml

from logs import event_logger
import generate
from tasks.exceptions import UnassignableTaskSet, HighCriticalityTaskFailureException
from simulation import simulator
from simulation.exceptions import UnschedulableException


def run_for_batch(config_file, batch_number: int, should_plot):
    cores, generated_tasks = generate.generate(config_file)
    try:
        simulator.run_simulation(cores, should_plot=should_plot)
    except HighCriticalityTaskFailureException:
        event_logger.log_event('Simulation failed due to High criticality task failure')
        raise UnschedulableException


def run(config_file, should_plot=False):
    with open('global_config.yml', 'r') as f:
        global_config = yaml.safe_load(f)

    event_logger.setup(config_file)

    number_of_batches = global_config['number_of_batches'] * 100
    # number_of_batches = 1
    has_already_plotted = False
    for rnd in tqdm.tqdm(range(number_of_batches)):
        try:
            run_for_batch(config_file, rnd, should_plot and not has_already_plotted)
            has_already_plotted = True
        except UnassignableTaskSet:
            event_logger.log_failed_task_assignment()
        except UnschedulableException:
            event_logger.log_failed_scheduling()
        finally:
            if rnd < number_of_batches - 1:
                event_logger.next_batch()

    event_logger.log_records('logs/records')
    event_logger.close()


if __name__ == '__main__':

    # run('configs/3.1.yml')
    # exit(0)

    if len(sys.argv) > 4:
        print('Usage: python run.py {CONFIG_FILE} {plot}, or just python run.py to run everything!')
        exit(1)
    if len(sys.argv) == 1:
        for file in os.listdir('configs'):
            run(f'configs/{file}')
    else:
        if len(sys.argv) == 3 and sys.argv[2] == 'plot':
            run(sys.argv[1], should_plot=True)
        else:
            run(sys.argv[1])
