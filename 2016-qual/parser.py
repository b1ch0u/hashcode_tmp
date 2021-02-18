from memoize import Memorize


@Memorize
def parse(in_file):
    with open(in_file) as f:
        lines = [line for line in f]
    
    res = {}
    
    rows_nb, columns_nb, drones_nb, max_time, max_load = map(int, lines.pop(0).split(' '))
    res['rows_nb'] = rows_nb
    res['columns_nb'] = columns_nb
    res['drones_nb'] = drones_nb
    res['max_time'] = max_time
    res['max_load'] = max_load

    res['products_nb'] = int(lines.pop(0))
    res['weights'] = list(map(int, lines.pop(0).split(' ')))

    res['warehouses_nb'] = int(lines.pop(0))
    res['warehouses'] = []
    for _ in range(res['warehouses_nb']):
        sub_res = {}
        row, col = map(int, lines.pop(0).split(' '))
        availabality = list(map(int, lines.pop(0).split(' ')))
        sub_res['row'] = row
        sub_res['col'] = col
        sub_res['availability'] = availabality
        res['warehouses'].append(sub_res)
    
    res['orders_nb'] = int(lines.pop(0))
    res['orders'] = []
    for _ in range(res['orders_nb']):
        sub_res = {}
        row, col = list(map(int, lines.pop(0).split(' ')))
        size = int(lines.pop(0))
        items = list(map(int, lines.pop(0).split(' ')))
        sub_res['row'] = row
        sub_res['col'] = col
        sub_res['size'] = size
        sub_res['col'] = col
        res['orders'].append(sub_res)
    
    return res