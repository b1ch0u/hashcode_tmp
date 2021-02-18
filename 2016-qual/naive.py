import math
import copy

def find_next_drone_available(drones):
    return drones.index(min(drones))

def distance_coord(start, end):
    xsrc, ysrc = start
    xdst, ydst = end

    return math.ceil(math.sqrt((xsrc -xdst)**2+(ysrc-ydst)**2))

def find_nearest_product(order,product_id,warehouses):
    # return the index of the nearest warehouse with product_id available
    warehouse_to_compare = []
    warehouse_distance = []
    for i in range(len(warehouses)):
        if warehouses[i]['availability'][product_id] != 0:
            warehouse_to_compare.append(i)
            start = warehouses[i]['row'], warehouses[i]['col']
            end = order['row'], order['col']
            warehouse_distance.append(distance_coord(start,end))
    return warehouse_to_compare[warehouse_distance.index(min(warehouse_distance))]

def compute_time_to_deliver(data,drone,drone_order,order):
    drone_location = drone.location
    duration = 0
    for load in drone_order:
        wh_first, item_first = load.first()
        duration += distance(drone_location,data['warehouses'][wh_first])
        duration += len(load)
        duration += distance(data['warehouses'][wh_first], order)
        duration += len(load)


def naive_solution(d):
    data = copy.deepcopy(d)
    sol_order = []
    queue_order = data['orders']
    drone_availability = data['drones_nb'] * [0]
    for order in d['orders']:
        drone_order = []
        drone_id = find_next_drone_available(drone_availability)
        warehouse_loads = [] # array of (warehouse_id,item_id)
        for item_id in order['items']:
            warehouse_id = find_nearest_product(order,item_id,data['warehouses'])
            wh_pickup = (warehouse_id,item_id)
            warehouse_loads.append(wh_pickup)
            data['warehouses'][warehouse_id]['availability'][item_id] -= 1
        drone_capacity = 0
        for load in warehouse_loads:
            drone_current_loading = []
            wh_id, item_id = load
            if (drone_capacity + data['weights'][item_id]) <= d['max_load']:
                drone_current_loading.append(load)
            else:
                drone_order.append(drone_current_loading)
                drone_current_loading = []
        if drone_current_loading:
            drone_order.append(drone_current_loading)