import os
import sys
import time

import psutil

from utils import gap_penalty, mismatch_penalty, parse_input, calculatePenalty, compare_output, generate_output, generate_plot_seq_list


def dp_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)
    opt = [[0 for j in range(n + 1)] for i in range(m + 1)]
    forward_record = [[0 for j in range(n + 1)] for i in range(m + 1)]

    for i in range(m + 1):
        opt[i][0] = i * gap_penalty
    for j in range(n + 1):
        opt[0][j] = j * gap_penalty

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            case_1 = mismatch_penalty(seq_x[i - 1], seq_y[j - 1]) + opt[i - 1][j - 1]
            case_2 = gap_penalty + opt[i - 1][j]
            case_3 = gap_penalty + opt[i][j - 1]

            min_cost = min(case_1, case_2, case_3)
            opt[i][j] = min_cost

            if case_1 == min_cost:
                forward_record[i][j] = 1
            elif case_2 == min_cost:
                forward_record[i][j] = 2
            else:
                forward_record[i][j] = 3

    return opt[m][n], forward_record


def get_dp_alignment(seq_x, seq_y, forward_record):
    align_x = ""
    align_y = ""
    align_path = []

    i, j = len(seq_x), len(seq_y)

    while i >= 1 or j >= 1:
        align_path.append((i, j))
        move = forward_record[i][j]
        if move == 1:
            align_x = seq_x[i - 1] + align_x
            align_y = seq_y[j - 1] + align_y
            i = i - 1
            j = j - 1
        elif move == 2:
            align_x = seq_x[i - 1] + align_x
            align_y = "_" + align_y
            i = i - 1
        elif move == 3:
            align_x = "_" + align_x
            align_y = seq_y[j - 1] + align_y
            j = j - 1
        else:
            if j >= 1:
                align_x = "_" + align_x
                align_y = seq_y[j - 1] + align_y
                j = j - 1
            elif i >= 1:
                align_x = seq_x[i - 1] + align_x
                align_y = "_" + align_y
                i = i - 1
            else:
                break

    align_path.append((i, j))
    return align_x, align_y, align_path


def run(sequences):
    start_time = time.time()
    cost, forward_info = dp_alignment(*sequences)
    align_x, align_y, alignment_path = get_dp_alignment(*sequences, forward_record=forward_info)
    end_time = time.time()
    time_sec = end_time - start_time

    process = psutil.Process(os.getpid())
    mem_kb = process.memory_info().rss / 1024.0  # in KB

    return align_x, align_y, cost, time_sec, mem_kb


def plot(n=21):
    with open('plot-basic.txt', 'w') as f:
        for i in range(1, n):
            sequences, problem_size = generate_plot_seq_list(i)
            align_x, align_y, cost, time_sec, mem_kb = run(sequences)
            f.write(str(problem_size) + "\t" + str(time_sec) + "\t" + str(mem_kb) + "\n")


if __name__ == '__main__':
    input_filename = sys.argv[1]
    seq_list = parse_input(input_filename)

    alignment_x, alignment_y, opt_cost, time_used, mem_used = run(seq_list)

    generate_output(alignment_x, alignment_y, str(opt_cost), str(time_used), str(mem_used))
    # plot()
