import math
import os
import sys

import psutil

from input_handler import parseInput
from utils import gap_penalty, mismatch_penalty, calculatePenalty, compare_output
from dp_solution import dp_alignment, get_dp_alignment


def space_efficient_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)
    cost_record = [[j * gap_penalty, 0] for j in range(n + 1)]
    last_line = [0 for j in range(n + 1)]

    for j in range(1, n + 1):
        cost_record[0][1] = j * gap_penalty
        for i in range(1, m + 1):
            cost_1 = mismatch_penalty(seq_x[i - 1], seq_y[j - 1]) + cost_record[i - 1][0]
            cost_2 = gap_penalty + cost_record[i - 1][1]
            cost_3 = gap_penalty + cost_record[i][0]
            cost_record[i][1] = min(cost_1, cost_2, cost_3)
        for i in range(m):
            cost_record[i][0] = cost_record[i][1]

    for j in range(1, n + 1):
        last_line[j] = cost_record[j][1]

    return last_line


def dc_alignment(seq_x, seq_y):
    align_x = ""
    align_y = ""
    m, n = len(seq_x), len(seq_y)

    if m == 0:
        for i in range(n):
            align_x = align_x + "_"
            align_y = align_y + seq_y[i]
    elif n == 0:
        for j in range(m):
            align_x = align_x + seq_x[j]
            align_y = align_y + "_"

    elif m == 1 or n == 1:
        opt_cost, forward_info = dp_alignment(seq_x, seq_y)
        align_x, align_y, alignment_path = get_dp_alignment(seq_x, seq_y, forward_record=forward_info)

    else:
        x_mid = int(math.floor(m / 2))

        cost_left = space_efficient_alignment(seq_x[:x_mid], seq_y)
        cost_right = space_efficient_alignment(seq_x[x_mid:][::-1], seq_y[::-1])

        y_mid = 0
        min_cost = sys.maxsize

        for j in range(1, n + 1):
            curr_cost = cost_left[j] + cost_right[j]
            if curr_cost < min_cost:
                min_cost = curr_cost
                y_mid = j - 1

        align_x_left, align_y_left = dc_alignment(seq_x[:x_mid], seq_y[:y_mid])
        align_x_right, align_y_right = dc_alignment(seq_x[x_mid:], seq_y[y_mid:])
        align_x = align_x_left + align_x_right
        align_y = align_y_left + align_y_right

    return align_x, align_y


if __name__ == '__main__':
    input_filename = "test_cases/input1.txt"
    seq_list = parseInput(input_filename)

    alignment_x, alignment_y = dc_alignment(*seq_list)
    print(alignment_x)
    print(alignment_y)
    print(calculatePenalty(alignment_x, alignment_y))
