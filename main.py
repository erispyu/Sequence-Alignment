import sys
from input_handler import parseInput

gap_penalty = 30

letter_dict = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}

mismatch_penalty = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]


def _mismatch_penalty(xi, yj):
    return mismatch_penalty[letter_dict[xi]][letter_dict[yj]]


def dp_alignment(seq_x, seq_y):
    m = len(seq_x)
    n = len(seq_y)
    opt = [[0 for j in range(n + 1)] for i in range(m + 1)]

    for i in range(m + 1):
        opt[i][0] = i * gap_penalty
    for j in range(n + 1):
        opt[0][j] = j * gap_penalty

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            case_1 = _mismatch_penalty(seq_x[i - 1], seq_y[j - 1]) + opt[i - 1][j - 1]
            case_2 = gap_penalty + opt[i - 1][j]
            case_3 = gap_penalty + opt[i][j - 1]
            opt[i][j] = min(case_1, case_2, case_3)

    return opt[m][n]


if __name__ == '__main__':
    input_filename = input("Please type in the path of input file: ") or "test_cases/input1.txt"
    print("input file is: " + input_filename)

    seq_list = parseInput(input_filename)
    dp_alignment(*seq_list)
