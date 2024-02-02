import os

import yaml

from logs import event_logger
import generate
from tasks.exceptions import UnassignableTaskSet, HighCriticalityTaskFailureException
from simulation import simulator
from simulation.exceptions import UnschedulableException


def run_for_batch(config_file, batch_number: int):
    cores, generated_tasks = generate.generate(config_file)
    try:
        simulator.run_simulation(cores)
    except HighCriticalityTaskFailureException:
        event_logger.log_event('Simulation failed due to High criticality task failure')
        raise UnschedulableException


def run(config_file):
    with open('global_config.yml', 'r') as f:
        global_config = yaml.safe_load(f)

    event_logger.setup(config_file)

    number_of_batches = global_config['number_of_batches']
    number_of_batches = 1

    for rnd in range(number_of_batches):
        print(f"====================\nBatch {rnd}\n====================")
        try:
            run_for_batch(config_file, rnd)
            if rnd < number_of_batches - 1:
                event_logger.next_batch()
        except UnassignableTaskSet:
            event_logger.log_failed_task_assignment()
        except UnschedulableException:
            event_logger.log_failed_scheduling()

    event_logger.close()


if __name__ == '__main__':
    # for file in os.listdir('configs'):
    #     run(f'configs/{file}')
    run('configs/1.1.yml')
