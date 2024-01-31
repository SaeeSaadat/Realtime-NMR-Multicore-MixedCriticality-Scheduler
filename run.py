import os

import yaml

from logs import event_logger
import generate
from tasks.exceptions import UnassignableTaskSet, HighCriticalityTaskFailureException
from simulation import simulator
from simulation.exceptions import UnschedulableException


def run_for_batch(config_file, batch_number: int):
    cores, generated_tasks = generate.generate(config_file)
    if cores is None:
        print(f"{batch_number} is unassignable")
        raise UnassignableTaskSet

    try:
        simulator.run_simulation(cores)
    except HighCriticalityTaskFailureException:
        raise UnschedulableException


def run(config_file):
    with open('global_config.yml', 'r') as f:
        global_config = yaml.safe_load(f)

    event_logger.setup(config_file)

    number_of_batches = global_config['number_of_batches']
    failed_assign_count = 0
    failed_scheduled_count = 0
    for rnd in range(number_of_batches):
        print(f"====================\nBatch {rnd}\n====================")
        try:
            run_for_batch(config_file, rnd)
            if rnd < number_of_batches - 1:
                event_logger.next_batch()
        except UnassignableTaskSet:
            # print(f"{rnd} is unassignable")
            failed_assign_count += 1
            failed_scheduled_count += 1
        except UnschedulableException:
            # print(f"{rnd} is unschedulable")
            failed_scheduled_count += 1

    with open(f'logs/{config_file}/stats', 'w') as f:
        f.write(f"Failed Assignments: {failed_assign_count}\n")
        f.write(f"Failed Schedulings: {failed_scheduled_count}")

    event_logger.close()


if __name__ == '__main__':
    # list of all files in configs folder
    for file in os.listdir('configs'):
        run(f'configs/{file}')
