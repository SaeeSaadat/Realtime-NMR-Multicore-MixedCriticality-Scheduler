"""
to calculate the number of copies needed:

Reliability = 1 - P ^ n
=> log (1 - R) / log (P)
N = ceil(-log(1 - R) / log(P)) if P ≠ 0, else 0
"""

import math


def calculated_number_of_copies(reliability, task_failure_probability):
    if task_failure_probability == 0:
        return
    return math.ceil(math.log2(1 - reliability) / math.log2(task_failure_probability))


if __name__ == '__main__':
    print(calculated_number_of_copies(0.9999999, 0.3))
