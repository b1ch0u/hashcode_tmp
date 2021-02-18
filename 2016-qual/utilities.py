import math
import copy


def distance(source, destination):
    xsrc, ysrc = source.location
    xdst, ydst = destination.location

    return math.ceil((math.sqrt((xsrc -xdst)**2+(ysrc-ydst)**2)))


def get_closest_order(d):
    #hypothetically fastest??? 
    b=distance(get_closest_warehouse_with_all_items(d,d["orders"][0],d["warehouse"]),d["orders"][0].location)
    bo=d["orders"][0]
    for o in d["orders"]:
        dist=distance(get_closest_warehouse_with_all_items(d,o,d["warehouse"]),o.location)
        if b>dist: #si la distance de l'order qu'on check est plus petite on prefere cette order la
            bo=o
            b=dist
        elif b==dist and get_nb_of_drones(bo,d)>get_nb_of_drones(o,d):#si même distance on prend celle avec le moins de drones
            bo = o
            b = dist
    return bo
    #la plus proche & qui a besoin du moins de drones ( si distances egales)


def get_cost_o(o,d):
        return distance(get_closest_warehouse_with_all_items(d,o,d["warehouse"]),o.location)*get_nb_of_drones(o,d)



def get_nb_of_drones(o,d):
    total_weight= sum(d['weights'][item] for item in o.items)
    return int(total_weight/d["max_load"])
    



def get_closest_warehouse_with_all_items(d,o,ws):
    #entries : d data, o order.
    #given an order, gives the nearest warehouse with all of the item if it exists
    #si aucune des warehouse n'a tous les items en stock alors retourne -1
    wh=get_closest_w(ws,o.location)
    for w in wh:
        yena=True
        for i in o.items:
            if(w.availability[i]<=0):
                yena=False
        if(yena):
            return w
    return -1 ####Pas pris en compte


def get_closest_w(warehouses, loc):
    #given a location and a list of warehouses gives a list ordered from the nearest warehouse to the furthest.
    m = distance([0], loc)
    wh = copy.deepcopy(warehouses)
    wh.sort(key=lambda w: distance(w,loc))
    return wh


def closest_drone(d,w):



instr=[] #list d'instrcutions (drone, action, warehouse, product type, nb product)

sorted_orders = copy.deepcopy(d["orders"])
sorted_orders.sort(key=lambda o: get_cost_o(d,o))
for o in sorted_orders:
    if(get_closest_warehouse_with_all_items(d,o,d["warehouses"])!=-1):
            
