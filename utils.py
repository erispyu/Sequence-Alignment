gap_penalty = 30

_letter_dict = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}

_mismatch_penalty_matrix = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]


def mismatch_penalty(xi, yj):
    return _mismatch_penalty_matrix[_letter_dict[xi]][_letter_dict[yj]]


def calculatePenalty(align_x, align_y):
    m, n = len(align_x), len(align_y)
    penalty = 0

    for i in range(m):
        x = align_x[i]
        y = align_y[i]
        if x == "_" or y == "_":
            penalty += gap_penalty
        else:
            penalty += mismatch_penalty(x, y)

    return penalty
