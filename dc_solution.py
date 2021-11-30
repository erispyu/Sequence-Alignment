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

    for j in reversed(range(n)):
        cost_record[0][1] = j * gap_penalty
        for i in reversed(range(m)):
            cost_1 = mismatch_penalty(seq_x[i], seq_y[j]) + cost_record[i + 1][0]
            cost_2 = gap_penalty + cost_record[i + 1][1]
            cost_3 = gap_penalty + cost_record[i][0]
            cost_record[i][1] = min(cost_1, cost_2, cost_3)
        for i in range(n + 1):
            cost_record[i][0] = cost_record[i][1]

    return cost_record


def dc_alignment(seq_x, seq_y, p_list):
    m, n = len(seq_x), len(seq_y)

    if m <= 2 or n <= 2:
        cost, path = dp_alignment(seq_x, seq_y)
        align_x, align_y = get_dp_alignment(seq_x, seq_y, path)
        return cost, align_x, align_y

    forward_cost = space_efficient_alignment(seq_x, seq_y[:n / 2])
    backward_cost = backward_space_efficient_alignment(seq_x, seq_y[n / 2:])

    min_cost = sys.maxsize
    q = 0
    for i in range(1, n + 1):
        curr_cost = forward_cost[i][n / 2] + backward_cost[i][n / 2]
        if curr_cost < min_cost:
            min_cost = curr_cost
            q = i

    p_list.append((q, n / 2))

    dc_alignment(seq_x[:q], seq_y[:n / 2], p_list)
    dc_alignment(seq_x[q:], seq_y[:n / 2:], p_list)
    return p_list


if __name__ == '__main__':
    input_filename = "test_cases/input1.txt"
    seq_list = parseInput(input_filename)

    result = dc_alignment(*seq_list, p_list=[])
    print(result)

