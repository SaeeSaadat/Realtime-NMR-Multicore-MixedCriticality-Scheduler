"""
This file is used to generate the task set for the simulation, using UUnifast algorithm.
This code has been based on this source: https://github.com/abolfazl9403/task_generation/blob/main/uunifast.py
"""

import random
from typing import List


def generate_uunifast_discard(u: float, n: int) -> List[float]:
    """
    Args:
        -   n  : The number of tasks in a task set.
        -   u  : Total utilization of the task set.
        -   num_sets  : Number of sets to generate.
    Returns   num_sets   of   n   task utilizations.
    """
    num_of_tries = 0
    while True:
        utilizations = []
        sum_u = u
        for i in range(1, n):
            next_sum_u = sum_u * random.random() ** (1.0 / (n - i))
            utilizations.append(sum_u - next_sum_u)
            sum_u = next_sum_u
        utilizations.append(sum_u)

        if all(ut <= 1 for ut in utilizations):
            return utilizations
        num_of_tries += 1
        if num_of_tries > 10000:
            raise Exception("Number of tries to generate tasks exceeded 1000")

