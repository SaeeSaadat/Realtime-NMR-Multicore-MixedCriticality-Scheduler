from typing import Dict, List
import math
import random

import tasks


def calculate_failures(cores: List[tasks.Processor], p_fail: float, hyper_period: int) -> Dict[int, tasks.Processor]:
    num_of_fails = round(len(cores) * p_fail)
    failed_cores = random.sample(cores, num_of_fails)
    fail_times = sorted([random.randint(0, hyper_period) for _ in range(num_of_fails)])
    return {fail_time: core for fail_time, core in zip(fail_times, failed_cores)}

