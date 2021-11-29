def compare(filename, align_x, align_y):
    align_headers = []
    align_tails = []

    length = 50

    align_headers.append(align_x[:length])
    align_tails.append(align_x[-length:])

    align_headers.append(align_y[:length])
    align_tails.append(align_y[-length:])

    with open(filename, 'r') as f:
        headers = f.readline().strip().split()
        tails = f.readline().strip().split()

    for i in range(2):
        print("********************************** Headers **********************************")
        print(align_headers[i])
        print(headers[i])
        print("*********************************** Tails ***********************************")
        print(align_tails[i])
        print(tails[i])
