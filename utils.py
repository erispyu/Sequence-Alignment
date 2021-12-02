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


def compare_output(filename, align_x, align_y):
    align_headers = []
    align_tails = []

    length = 50

    align_headers.append(align_x[:length])
    align_tails.append(align_x[-length:])

    align_headers.append(align_y[:length])
    align_tails.append(align_y[-length:])

    with open(filename, 'r') as f:
        given_align_x = f.readline().strip().split()
        given_align_y = f.readline().strip().split()

    print("****************************** Align x: Headers ******************************")
    print(align_headers[0])
    print(given_align_x[0])
    print("******************************* Align x: Tails *******************************")
    print(align_tails[0])
    print(given_align_x[1])

    print("****************************** Align y: Headers ******************************")
    print(align_headers[1])
    print(given_align_y[0])
    print("******************************* Align y: Tails *******************************")
    print(align_tails[1])
    print(given_align_y[1])
