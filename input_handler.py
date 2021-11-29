def parseInput(filename):
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


def _generate_sequence(base_string, generate_rule):
    sequence = base_string
    for rule in generate_rule:
        sequence = sequence[:rule + 1] + base_string + sequence[rule + 1:]
        base_string = sequence
    return sequence
