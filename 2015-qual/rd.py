import random as rd
from copy import deepcopy

def randomly_change_one_assignation(d, sol):
    rows_content, pools_content = sol
    non_empty_pools_indexes = [i for i, pool in enumerate(pools_content) if pool]
    pool_number = rd.choice(non_empty_pools_indexes)
    server_index = rd.randint(0, len(pools_content[pool_number])-1)
    pool_number_add = rd.randint(0, len(pools_content) - 1)
    while pool_number_add == pool_number:
        pool_number_add = rd.randint(0, len(pools_content) - 1)
    pools_content[pool_number_add].append(pools_content[pool_number][server_index])
    pools_content[pool_number].pop(server_index)


def rd_improve_sol(d, N, rows_content, pools_content, score_function, modif_func, eps=0):
    current_sol = (rows_content, pools_content)
    best_score = score_function(d, current_sol)
    best_sol = current_sol
    for i in range(1, N + 1):
        if i % 5000 == 0: print(f'iteration {i}, current score {best_score}')
        pools_content_copy = deepcopy(pools_content)
        modif_func(d, (rows_content, pools_content_copy))
        new_score = score_function(d, (rows_content, pools_content_copy))
        if new_score >= best_score:
            if new_score > best_score:
                print('new best score:', new_score)
            best_score = new_score
            pools_content = pools_content_copy
            best_sol = (rows_content, pools_content)
        elif rd.random() < eps:
            pools_content = pools_content_copy
    return best_score, best_sol