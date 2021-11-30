import os
import psutil

from input_handler import parseInput
from utils import gap_penalty, mismatch_penalty, calculatePenalty, compare_output


def dc_alignment(seq_x, seq_y):
    print(seq_x, seq_y)


if __name__ == '__main__':
    input_filename = "test_cases/input1.txt"
    seq_list = parseInput(input_filename)
