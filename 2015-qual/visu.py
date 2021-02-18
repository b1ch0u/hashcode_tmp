def print_first_row(d, sol):
    # print of unavailable slots index

    print("Index of unavailable slots:")
    first_row_unavail_slots_index = []
    for una in d['unvailables']:
        if una['row'] == 0:
            first_row_unavail_slots_index.append(una['col'])
    print(first_row_unavail_slots_index)
