import os
import sys
from typing import Optional

import tqdm
import yaml

from logs import event_logger
import generate
import tasks
from tasks.exceptions import UnassignableTaskSet, HighCriticalityTaskFailureException
from simulation import simulator, execution_table
from simulation.exceptions import UnschedulableException

records = {}


def register_records(rnd: int, mode: str, exec_table: Optional[execution_table.ExecutionTable], unassignable=False):
    if exec_table is None:
        quality_of_service = None
        is_schedulable = False
    else:
        quality_of_service = exec_table.average_qos
        is_schedulable = exec_table.is_schedulable
    if mode not in records:
        records[mode] = {}
    records[mode][rnd] = {
        'qos': quality_of_service,
        'schedulable': is_schedulable,
        'assignable': not unassignable
    }


def dump_records():
    with open('final_records_full.yml', 'w') as f:
        yaml.dump(records, f)
    with open('final_records.yml', 'w') as f:
        yaml.dump({k: v['result'] for k, v in records.items()}, f)


def run_for_batch(config_file, batch_number: int, should_plot, edf_only=False):
    config = tasks.ProjectConfig(config_file)
    cores, generated_tasks = generate.generate(config)
    try:
        exec_table = simulator.run_simulation(cores, should_plot=should_plot,
                                              overrun_probability=config.overrun_percentage,
                                              task_fail_probability=config.error_rate,
                                              edf_only=edf_only
                                              )
        event_logger.log_event('Simulation completed successfully')
        return exec_table
    except HighCriticalityTaskFailureException:
        event_logger.log_event('Simulation failed due to High criticality task failure')
        raise UnschedulableException


def run(config_file, should_plot=False, edf_only=False):
    with open('global_config.yml', 'r') as f:
        global_config = yaml.safe_load(f)

    event_logger.setup(config_file)
    mode = f'{".".join(config_file.split("/")[-1].split(".")[:-1])}{"-EDF" if edf_only else "-EDF-VD"}'

    number_of_batches = global_config['number_of_batches']
    has_already_plotted = False
    for rnd in tqdm.tqdm(range(number_of_batches)):
        try:
            exec_table = run_for_batch(config_file, rnd, should_plot and not has_already_plotted, edf_only=edf_only)
            register_records(rnd=rnd, mode=mode, exec_table=exec_table)
            has_already_plotted = True
        except UnassignableTaskSet:
            event_logger.log_failed_task_assignment()
            register_records(rnd=rnd, mode=mode, exec_table=None, unassignable=True)
        except UnschedulableException:
            event_logger.log_failed_scheduling()
            register_records(rnd=rnd, mode=mode, exec_table=None)
        finally:
            if rnd < number_of_batches - 1:
                event_logger.next_batch()

    event_logger.log_records('logs/records')
    event_logger.close()
    if mode not in records:
        records[mode] = {}
    records[mode]['result'] = {
        'avg QoS': sum([v['qos'] for v in records[mode].values() if v['qos'] is not None]) / number_of_batches,
        'schedulable rate': sum([1 if v['schedulable'] else 0 for v in records[mode].values()]) / number_of_batches,
        'assignable rate': sum([1 if v['assignable'] else 0 for v in records[mode].values()]) / number_of_batches,
        'schedulable count': f"{sum([1 if v['schedulable'] else 0 for v in records[mode].values()])} / {number_of_batches}",
        'assignable count': f"{sum([1 if v['assignable'] else 0 for v in records[mode].values()])} / {number_of_batches}"
    }


def main():
    if len(sys.argv) > 4:
        print('Usage: python run.py {CONFIG_FILE} {plot}, or just python run.py to run everything!')
        exit(1)
    if len(sys.argv) == 1:
        for file in os.listdir('configs'):
            print(f'Running {file}')
            run(f'configs/{file}')
            run(f'configs/{file}', edf_only=True)
    else:
        if len(sys.argv) == 3:
            if sys.argv[2] == 'plot':
                run(sys.argv[1], should_plot=True)
            elif sys.argv[2] == 'edf-only':
                run(sys.argv[1], edf_only=True, should_plot=True)

        else:
            run(sys.argv[1])

    dump_records()


if __name__ == '__main__':
    main()
