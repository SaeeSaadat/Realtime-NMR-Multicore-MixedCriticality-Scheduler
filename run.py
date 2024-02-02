import os
import sys

import tqdm
import yaml

from logs import event_logger
import generate
import tasks
from tasks.exceptions import UnassignableTaskSet, HighCriticalityTaskFailureException
from simulation import simulator
from simulation.exceptions import UnschedulableException


def run_for_batch(config_file, batch_number: int, should_plot, edf_only=False):
    config = tasks.ProjectConfig(config_file)
    cores, generated_tasks = generate.generate(config)
    try:
        simulator.run_simulation(cores, should_plot=should_plot,
                                 overrun_probability=config.overrun_percentage,
                                 task_fail_probability=config.error_rate,
                                 edf_only=edf_only
                                 )
    except HighCriticalityTaskFailureException:
        event_logger.log_event('Simulation failed due to High criticality task failure')
        raise UnschedulableException


def run(config_file, should_plot=False, edf_only=False):
    with open('global_config.yml', 'r') as f:
        global_config = yaml.safe_load(f)

    event_logger.setup(config_file)

    number_of_batches = global_config['number_of_batches']
    # number_of_batches = 1
    has_already_plotted = False
    for rnd in tqdm.tqdm(range(number_of_batches)):
        try:
            run_for_batch(config_file, rnd, should_plot and not has_already_plotted, edf_only=edf_only)
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
        if len(sys.argv) == 3:
            if sys.argv[2] == 'plot':
                run(sys.argv[1], should_plot=True)
            elif sys.argv[2] == 'edf-only':
                run(sys.argv[1], edf_only=True, should_plot=True)

        else:
            run(sys.argv[1])
