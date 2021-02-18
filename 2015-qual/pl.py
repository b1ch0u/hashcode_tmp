from memoize import Memorize

from assign import *


global_data = {}


@Memorize
def assign_to_row():
    #  TODO mélanger avant (et remettre dans le bon ordre à la fin) pour randomiser un peu
    global global_data
    d = global_data
    block_sizes = []
    server_sizes = []
    server_capacities = []
    for block in d['blocks']:
        block_sizes.append(block['size'])
    for server in d['servers']:
        server_sizes.append(server['size'])
        server_capacities.append(server['capacity'])
    
    _, _, blocks_content = solve_multi_knapsack(block_sizes, server_sizes, server_capacities)
    return blocks_content


def pl_assign(d, coeff):
    global global_data
    global_data = d
    # import pprint
    # pprint.pprint(d)
    _, _, blocks_content = assign_to_row()

    # rebuild rows
    rows_content = [[] for _ in range(d['rows_nb'])]
    for i, block in enumerate(blocks_content):
        rows_content[d['blocks'][i]['row']].extend(block)

    return rows_content