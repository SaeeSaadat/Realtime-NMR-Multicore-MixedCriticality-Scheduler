"""

IMPORTANT NOTE:
This project will use TMR instead of NMR going forward.
therefor this file is no longer used except for the first function which just returns 3 (THREE modular redundancy)


to calculate the number of copies needed:

Reliability = 1 - P ^ n
=> log (1 - R) / log (P)
N = ceil(-log(1 - R) / log(P)) if P ≠ 0, else 0
"""
import math


def calculated_number_of_copies(reliability, task_failure_probability):
    return 3

    # if task_failure_probability == 0:
    #     return 1
    # return math.ceil(math.log2(1 - reliability) / math.log2(task_failure_probability))


def r_i(wcet, fault_rate):
    # reliability of a task
    return math.e ** (-fault_rate * wcet)


def calculate_number_of_copies():
    failure_rate = 0.3
    wcet = 10
    task_reliability = r_i(wcet, failure_rate)
    # print("task reliability", task_reliability)
    task_failure_probability = 1 - task_reliability
    for n in range(1, 20):
        fault_free_reliability = task_reliability ** math.ceil(n / 2)
        faulty_reliability = sum(
            math.comb(n, i) * (task_failure_probability ** i) * (
                    (1 - task_failure_probability) ** i) * (task_reliability ** (n - i))
            for i in range(1, math.floor(n / 2) + 1)
        )
        total_reliability = fault_free_reliability + faulty_reliability
        # print(fault_free_reliability, '\t', faulty_reliability, '\t', total_reliability)


def calculate_based_on_formulas(wcet_hi, wcet_lo):
    landa_0 = 0.0001
    d = 2
    f = 1
    f_min = 0.6
    alpha = 0.01
    PoF_target = 1 - 0.9999999

    landa = landa_0 * (10 ** (d * (1 - f) / (1 - f_min)))
    R_lo = (1 - alpha) * math.exp(-landa * wcet_lo)
    R_hi = (1 - alpha) * math.exp(-landa * wcet_hi)
    PoF_hi = 1 - R_hi
    PoF_lo = 1 - R_lo
    r_lower = int(math.log(PoF_target / PoF_hi) / math.log(PoF_lo))
    r_upper = int(math.log(PoF_target / PoF_hi) / math.log(PoF_hi))
    k = (r_lower + r_upper) // 2
    r = int(math.log((PoF_target / (PoF_hi ** (k + 1))) * (PoF_lo ** k)) / math.log(PoF_lo))
    return r


if __name__ == '__main__':
    # print(calculated_number_of_copies(0.9999999, 0.3))
    # calculate_number_of_copies()
    print(calculate_based_on_formulas(182.88263543073828,75.9823270084509))
