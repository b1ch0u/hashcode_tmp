import random as rd
import itertools as it


def compute_gc(d, pool, row_id_by_serv):
    pool_capacity = sum(d['servers'][serv]['capacity']
                        for serv in pool)
    max_capacity = max(sum(d['servers'][serv]['capacity']
                            for serv in pool
                            if row_id_by_serv[serv] == row_id)
                        for row_id in range(d['rows_nb']))
    return pool_capacity - max_capacity


def compute_gcs(d, rows, pools):
    servers_row = [None] * d['servers_nb']
    for i, row in enumerate(rows):
        for serv in row:
            servers_row[serv] = i

    gcs = [compute_gc(d, pool, servers_row)
            for pool in pools]

    return servers_row, gcs


def rd_assign_pools(d, rows, attributed_servers):
    pools = [[] for _ in range(d['pools_nb'])]
    for serv in attributed_servers:
        pools[rd.randint(0, d['pools_nb'] - 1)].append(serv)
    return pools


attributed_servers = []
row_id_by_serv = []
d = {}


class Solution:
    def __init__(self, t_d, rows, pools=None):
        global d
        global attributed_servers
        global row_id_by_serv
        d = t_d
        attributed_servers = tuple(serv for row in rows for serv in row)

        if pools is None:
            pools = rd_assign_pools(d, rows, attributed_servers)
        self.pools = pools
        self.pool_id_by_serv = {serv: i
                                for i, pool in enumerate(self.pools)
                                for serv in pool}
        row_id_by_serv, self.gcs = compute_gcs(d, rows, pools)
        self.score = min(self.gcs)
    
    def attribute_server(self, serv, dest_pool_id):
        current_pool_id = self.pool_id_by_serv[serv]
        if current_pool_id == dest_pool_id:
            return self.score
        self.pools[current_pool_id].remove(serv)
        self.pools[dest_pool_id].append(serv)
        self.pool_id_by_serv[serv] = dest_pool_id
        self.gcs[current_pool_id] = compute_gc(d,
                                                self.pools[current_pool_id],
                                                row_id_by_serv)
        self.gcs[dest_pool_id] = compute_gc(d,
                                            self.pools[dest_pool_id],
                                            row_id_by_serv)
        self.score = min(self.gcs)
        return self.score
    
    def apply(self, move):
        serv, dest_pool = move
        self.attribute_server(serv, dest_pool)
    
    def get_possible_moves(self):
        # peut renvoyer un iterable
        pools = [pool_id for pool_id in range(d['pools_nb'])
                if self.gcs[pool_id] <= self.score]
        # if rd.random() < 1/10: print('nb of critical pools', len(pools))
        non_critical_servers = [serv for serv in attributed_servers
                                if all(serv not in self.pools[pool] for pool in pools)]
        moves = []
        for pool in pools:
            # ps = self.gcs[pool]
            # critical_rows = [row for row in ]
            for serv in non_critical_servers:
                if serv not in self.pools[pool]:
                    moves.append((serv, pool))
        # print('len of moves', len(moves))
        rd.shuffle(moves)
        moves = moves[:25]
        return moves