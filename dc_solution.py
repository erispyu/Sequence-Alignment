import math
import os
import sys

import psutil

from input_handler import parseInput
from utils import gap_penalty, mismatch_penalty, calculatePenalty, compare_output
from dp_solution import dp_alignment, get_dp_alignment


def space_efficient_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)
    cost_record = [[i * gap_penalty, 0] for i in range(m + 1)]

    for j in range(1, n + 1):
        cost_record[0][1] = j * gap_penalty
        for i in range(1, m + 1):
            cost_1 = mismatch_penalty(seq_x[i - 1], seq_y[j - 1]) + cost_record[i - 1][0]
            cost_2 = gap_penalty + cost_record[i - 1][1]
            cost_3 = gap_penalty + cost_record[i][0]
            cost_record[i][1] = min(cost_1, cost_2, cost_3)
        for i in range(n + 1):
            cost_record[i][0] = cost_record[i][1]

    return cost_record


def backward_space_efficient_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)
    cost_record = [[i * gap_penalty, 0] for i in range(m + 1)]

    for j in reversed(range(n - 1)):
        cost_record[0][1] = j * gap_penalty
        for i in reversed(range(m - 1)):
            cost_1 = mismatch_penalty(seq_x[i], seq_y[j]) + cost_record[i + 1][0]
            cost_2 = gap_penalty + cost_record[i + 1][1]
            cost_3 = gap_penalty + cost_record[i][0]
            cost_record[i][1] = min(cost_1, cost_2, cost_3)
        for i in range(n + 1):
            cost_record[i][0] = cost_record[i][1]

    return cost_record


def dc_alignment(seq_x, seq_y, path):
    m, n = len(seq_x), len(seq_y)
    half_n = math.floor(n / 2)

    if m <= 2 or n <= 2:
        cost, forward_info = dp_alignment(seq_x, seq_y)
        align_x, align_y, path = get_dp_alignment(seq_x, seq_y, forward_info)
        return path

    forward_cost = space_efficient_alignment(seq_x, seq_y[:half_n])
    backward_cost = backward_space_efficient_alignment(seq_x, seq_y[half_n:])

    min_cost = sys.maxsize
    q = 0
    for i in range(1, m + 1):
        curr_cost = forward_cost[i][1] + backward_cost[i][1]
        if curr_cost < min_cost:
            min_cost = curr_cost
            q = i

    path.append((q, half_n))

    dc_alignment(seq_x[:q], seq_y[:half_n], path)
    dc_alignment(seq_x[q:], seq_y[half_n:], path)
    return path


if __name__ == '__main__':
    # input_filename = "test_cases/input1.txt"
    # seq_list = parseInput(input_filename)

    seq_list = ["AG", "AC"]

    result = dc_alignment(*seq_list, path=[])
    print(result)

