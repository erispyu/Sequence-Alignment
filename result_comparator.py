def compare(filename, align_x, align_y):
    align_headers = []
    align_tails = []

    align_headers.append(align_x[:51].replace("_", ""))
    align_tails.append(align_x[-51:].replace("_", ""))

    align_headers.append(align_y[:51].replace("_", ""))
    align_tails.append(align_y[-51:].replace("_", ""))

    with open(filename, 'r') as f:
        headers = f.readline().strip().replace("_", "").split()
        tails = f.readline().strip().replace("_", "").split()

    for i in range(2):
        print(align_headers[i] == headers[i])
        print(align_tails[i] == tails[i])
