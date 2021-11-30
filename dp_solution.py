import os
import psutil

from input_handler import parseInput
from utils import gap_penalty, mismatch_penalty, calculatePenalty, compare_output


def dp_alignment(seq_x, seq_y):
    m, n = len(seq_x), len(seq_y)
    opt = [[0 for j in range(n + 1)] for i in range(m + 1)]
    path_info = [[0 for j in range(n + 1)] for i in range(m + 1)]

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
                path_info[i][j] = 1
            elif case_2 == min_cost:
                path_info[i][j] = 2
            else:
                path_info[i][j] = 3

    return opt[m][n], path_info


def get_dp_alignment(seq_x, seq_y, path_info):
    align_x = ""
    align_y = ""
    i, j = len(seq_x), len(seq_y)
    while i >= 1 or j >= 1:
        move = path_info[i][j]
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
    return align_x, align_y


if __name__ == '__main__':
    # input_filename = input("Please type in the path of input file: ") or "test_cases/input1.txt"
    # print("input file is: " + input_filename)

    input_filename = "test_cases/input1.txt"

    seq_list = parseInput(input_filename)

    # seq_list = ["AGCT", "ACCT"]

    print("**************************** Generated Sequences ****************************")
    for seq in seq_list:
        print(seq)

    opt_cost, path = dp_alignment(*seq_list)
    alignment_x, alignment_y = get_dp_alignment(seq_list[0], seq_list[1], path)

    print("**************************** Alignments ****************************")
    print(alignment_x)
    print(alignment_y)

    print("**************************** Cost Comparation ****************************")
    print("Generated:\t" + str(opt_cost))
    print("Calculated:\t" + str(calculatePenalty(alignment_x, alignment_y)))

    compare_output("test_cases/output1.txt", alignment_x, alignment_y)

    process = psutil.Process(os.getpid())
    print(process.memory_info().rss)
