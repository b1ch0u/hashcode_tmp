import random as rd

def assign_server_from_max_to_min_guar_cap(d, sol):
    rows_content, pools_content = sol
    guarenteed_capacities = compute_guarenteed_capacity(d, sol)
    max_pool_index = guarenteed_capacities.index(max(guarenteed_capacities))
    min_pool_index = guarenteed_capacities.index(min(guarenteed_capacities))
    reassignated_server = pools_content[max_pool_index].pop(rd.randint(0,len(pools_content[max_pool_index])-1))
    pools_content[min_pool_index].append(reassignated_server)
    return rows_content, pools_content


# TODO calculer score max possible sur assignation obtenue

# TODO trouver le pool P1 avec le score le plus bas (ou choisir rd)
# trouver le pool P2 avec le score le plus haut (ou choisir rd)
# trouver la ligne L1 de P1 qui lui confère son score bas, et choisir un serveur S1 dedans
# trouver une ligne L2 de P2 (idéalement, qui n'est pas critique)
# trouver dans L2 un serveur de même taille que S1, ou approchant
# réassigner S1 à P2 et S2 à P1


def compute_guarenteed_capacity(d, sol):
    rows_content, pools_content = sol

    servers_row = [-1] * d['servers_nb']
    for i, row in enumerate(rows_content):
        for serv in row:
            servers_row[serv] = i

    gcs = []
    for pool in pools_content:
        pool_capacity = sum(d['servers'][serv]['capacity']
                            for serv in pool)
        max_capacity = max(sum(d['servers'][serv]['capacity']
                                for serv in pool
                                if servers_row[serv] == row_nb)
                            for row_nb in range(d['rows_nb']))
        gcs.append(pool_capacity - max_capacity)
    return gcs