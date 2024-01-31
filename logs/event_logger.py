from io import TextIOWrapper
import os

log_file: TextIOWrapper
config_name: str
batch_no: int = 1


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
