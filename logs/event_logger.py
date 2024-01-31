from io import TextIOWrapper

log_file: TextIOWrapper


def setup(log_file_name):
    global log_file
    log_file = open(log_file_name, 'w')


def close():
    global log_file
    if log_file is not None:
        log_file.close()


def log_event(event):
    global log_file
    if log_file is None:
        raise Exception('Event logger is not set up')

    log_file.write(event + '\n')


def log(time, event):
    global log_file
    if log_file is None:
        raise Exception('Event logger is not set up')

    log_event(f'{time:10.4f}: {event}')
