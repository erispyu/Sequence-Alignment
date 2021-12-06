import math
import os
import sys
import time

import psutil

from utils import gap_penalty, mismatch_penalty, parse_input, calculatePenalty, compare_output, generate_output
from basic import dp_alignment, get_dp_alignment


def space_efficient_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)
    cost_record = [[0 for j in range(n + 1)] for i in range(2)]
    last_line = [0 for j in range(n + 1)]

    for j in range(1, n + 1):
        cost_record[0][j] = j * gap_penalty

    for i in range(1, m + 1):
        cost_record[1][0] = cost_record[0][0] + gap_penalty
        for j in range(1, n + 1):
            cost_1 = mismatch_penalty(seq_x[i - 1], seq_y[j - 1]) + cost_record[0][j - 1]
            cost_2 = gap_penalty + cost_record[1][j - 1]
            cost_3 = gap_penalty + cost_record[0][j]
            cost_record[1][j] = min(cost_1, cost_2, cost_3)
        for j in range(n + 1):
            cost_record[0][j] = cost_record[1][j]

    for j in range(n + 1):
        last_line[j] = cost_record[1][j]

    return last_line


def dc_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)

    if m <= 2 or n <= 2:
        opt_cost, forward_info = dp_alignment(seq_x, seq_y)
        align_x, align_y, alignment_path = get_dp_alignment(seq_x, seq_y, forward_record=forward_info)

    else:
        x_mid = m / 2

        cost_left = space_efficient_alignment(seq_x[:x_mid], seq_y)
        cost_right = space_efficient_alignment(seq_x[x_mid:][::-1], seq_y[::-1])

        y_mid = None
        min_cost = sys.maxsize

        for j in range(1, n + 1):
            curr_cost = cost_left[j] + cost_right[n - j]
            if curr_cost < min_cost:
                min_cost = curr_cost
                y_mid = j

        align_x_left, align_y_left = dc_alignment(seq_x[:x_mid], seq_y[:y_mid])
        align_x_right, align_y_right = dc_alignment(seq_x[x_mid:], seq_y[y_mid:])
        align_x = align_x_left + align_x_right
        align_y = align_y_left + align_y_right

    return align_x, align_y


if __name__ == '__main__':
    input_filename = sys.argv[1]
    seq_list = parse_input(input_filename)

    start_time = time.time()
    alignment_x, alignment_y = dc_alignment(*seq_list)
    end_time = time.time()
    time_used = end_time - start_time

    # print(alignment_x)
    # print(alignment_y)
    # print(calculatePenalty(alignment_x, alignment_y))
    # compare_output("test_cases/output1.txt", alignment_x, alignment_y)

    opt_cost = calculatePenalty(alignment_x, alignment_y)

    process = psutil.Process(os.getpid())
    mem_used = process.memory_info().rss / 1024.0  # in KB

    generate_output(alignment_x, alignment_y, str(opt_cost), str(time_used), str(mem_used))
