def create_unavailable_positions(d):
    d['unp'] = set()
    for una in d['unavailables']:
        d['unp'].add((una['row'], una['col']))


def extract_blocks_from_row(d, row):
    res = []
    last_col = 0
    col = 0
    while col < d['slots_nb']:
        while col < d['slots_nb'] and (row, col) not in d['unp']:
            col += 1
        if col > last_col:
            res.append({
                'size': col - last_col,
                'row': row,
                'col': last_col
            })
        col += 1
        last_col = col
    return res
        

def precompute_blocks(d):
    d['blocks'] = []
    for row in range(d['rows_nb']):
        d['blocks'] += extract_blocks_from_row(d, row)
    d['blocks_ids_by_row'] = [ [] for row in range(d['rows_nb'])]
    for i, block in enumerate(d['blocks']):
        d['blocks_ids_by_row'][block['row']].append(i)


def enrich_data(data):
    create_unavailable_positions(data)
    precompute_blocks(data)