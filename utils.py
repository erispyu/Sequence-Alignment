from random import randint

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


def _generate_sequence(base_string, generate_rule):
    sequence = base_string
    for rule in generate_rule:
        sequence = sequence[:rule + 1] + base_string + sequence[rule + 1:]
        base_string = sequence
    return sequence


def parse_input(filename):
    sequence_list = []

    with open(filename, 'r') as f:
        base_string_x = f.readline().strip()
        generate_rule_x = []
        while True:
            line = f.readline().strip()
            if line.isdigit():
                generate_rule_x.append(int(line))
            else:
                base_string_y = line
                break
        sequence_list.append(_generate_sequence(base_string_x, generate_rule_x))

        generate_rule_y = []
        while True:
            line = f.readline().strip()
            if line.isdigit():
                generate_rule_y.append(int(line))
            else:
                break
        sequence_list.append(_generate_sequence(base_string_y, generate_rule_y))

    return sequence_list


def _tail_alignments(align_x, align_y, length = 50):
    tailed_align_x = align_x[:length] + " " + align_x[-length:]
    tailed_align_y = align_y[:length] + " " + align_y[-length:]

    return tailed_align_x, tailed_align_y


def generate_output(align_x, align_y, cost, time_used, mem_used):
    tailed_align_x, tailed_align_y = _tail_alignments(align_x, align_y)
    with open('output.txt', 'w') as f:
        f.write(tailed_align_x + "\n")
        f.write(tailed_align_y + "\n")
        f.write(cost + "\n")
        f.write(time_used + "\n")
        f.write(mem_used + "\n")


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


def generate_plot_seq_list(n):
    base_strings = ["ACTG", "TACG"]
    seq_list = []

    generate_rule_x = []
    generate_rule_y = []
    for i in range(n):
        rule_x = randint(1, 9)
        generate_rule_x.append(rule_x)
        rule_y = randint(1, 9)
        generate_rule_y.append(rule_y)

    seq_list.append(_generate_sequence(base_strings[0], generate_rule_x))
    seq_list.append(_generate_sequence(base_strings[1], generate_rule_y))

    problem_size = len(seq_list[0])

    return seq_list, problem_size

