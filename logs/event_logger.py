from io import TextIOWrapper
import os

log_file: TextIOWrapper
config_name: str
batch_no: int = 1

records = {}
execution_table = {}


def setup(conf_name):
    global log_file, config_name
    config_name = conf_name
    # create directory for logs/config_name
    if not os.path.exists(f'logs/{config_name}'):
        os.makedirs(f'logs/{config_name}')
    log_file = open(f'logs/{config_name}/batch_{batch_no}.schedule', 'w')


def next_batch():
    global batch_no, log_file
    # log_file.close()
    batch_no += 1
    log_file = open(f'logs/{config_name}/batch_{batch_no}.schedule', 'w')


def close():
    global log_file
    if log_file is not None:
        log_file.close()


def log_event(event):
    if log_file is None:
        raise Exception('Event logger is not set up')

    log_file.write(event + '\n')


def log(time, event):
    if log_file is None:
        raise Exception('Event logger is not set up')

    log_event(f'{time:10.0f}: {event}')


def record(key, value):
    global records
    records[key] = value


def log_records(file='logs/records'):
    with open(file, 'w') as f:
        for k, v in records.items():
            f.write(f'{k}: {v}\n')


def log_failed_scheduling():
    global records
    records['failed_scheduling'] = records.get('failed_scheduling', 0) + 1


def log_failed_task_assignment():
    global records
    records['failed_task_assignment'] = records.get('failed_task_assignment', 0) + 1