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
    # print("Generated tasks:")
    # for t in generated_tasks:
    #     print(t)
    # print("\n====================\n")
    # print("Core assignments:")
    # for c in cores:
    #     print(c.name, "\tUtilization:", c.utilization(), "\tTasks:", [t.name for t in c.tasks])
    # print("\n====================\n")

    for core in cores:
        print(core.calculate_edf_vd_constant())
    try:
        simulator.run_simulation(cores)
    except HighCriticalityTaskFailureException:
        raise UnschedulableException


def run(config_file):
    with open('configs/global_config.yml', 'r') as f:
        global_config = yaml.safe_load(f)

    event_logger.setup('logs/events.log')

    number_of_batches = global_config['number_of_batches']
    failed_assign_count = 0
    failed_scheduled_count = 0
    # for rnd in range(number_of_batches):
    for rnd in range(1):
        print(f"====================\nBatch {rnd + 1}\n====================")
        try:
            run_for_batch(config_file, rnd)
        except UnassignableTaskSet:
            print(f"{rnd} is unassignable")
            failed_assign_count += 1
            failed_scheduled_count += 1
        except UnschedulableException:
            print(f"{rnd} is unschedulable")
            failed_scheduled_count += 1


if __name__ == '__main__':
    run('configs/1.1.yml')
    # a = {1: ('s', 'b'), 2: (5, 6)}
    # for t, (m, n) in a.items():
    #     print(t, m, n)