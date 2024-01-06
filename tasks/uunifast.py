"""
This file is used to generate the task set for the simulation, using UUnifast algorithm.
This code has been based on this source: https://github.com/abolfazl9403/task_generation/blob/main/uunifast.py
"""

import csv
import random


def _write_to_csv(filename, sets, n):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Task ' + str(i) for i in range(1, n + 1)])
        for utilizations in sets:
            writer.writerow(utilizations)


def generate_uunifast_discard(nsets: int, u: float, n: int):
    """
    The UUniFast algorithm was proposed by Bini for generating task
    utilizations on uniprocessor architectures.
    The UUniFast-Discard algorithm extends it to multiprocessor by
    discarding task sets containing any utilization that exceeds 1.
    This algorithm is easy and widely used. However, it suffers from very
    long computation times when n is close to u. Stafford's algorithm is
    faster.
    Args:
        -   n  : The number of tasks in a task set.
        -   u  : Total utilization of the task set.
        -   nsets  : Number of sets to generate.
    Returns   nsets   of   n   task utilizations.
    """
    sets = []
    while len(sets) < nsets:
        utilizations = []
        sum_u = u
        for i in range(1, n):
            next_sum_u = sum_u * random.random() ** (1.0 / (n - i))
            utilizations.append(sum_u - next_sum_u)
            sum_u = next_sum_u
        utilizations.append(sum_u)

        if all(ut <= 1 for ut in utilizations):
            sets.append(utilizations)

    return sets


if __name__ == '__main__':
    task_utilizations = generate_uunifast_discard(nsets=5, u=0.75, n=10)
    _write_to_csv('task_utilizations.csv', task_utilizations, 10)
