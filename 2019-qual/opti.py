from collections import deque
import random as rd

import numpy as np
from python_tsp.heuristics import solve_tsp_simulated_annealing

from utils import compute_interest, Slide, Solution

def opti_permutation_slide(sol):
    for i in range(len(sol.slides)):
        if (i%100) == 0:
            print(i)
        for j in range(i+1, len(sol.slides)):
            new_score = compute_score_permutation_slide(sol,i,j)
            if  new_score > sol.score:
                sol.slides[i], sol.slides[j] = sol.slides[j], sol.slides[i]
                sol.score = new_score
    
    return sol


def compute_score_permutation_slide(sol,a, b): # permutation of slide index a and b with a<b
    interest_lost = 0
    interest_gained = 0
    if a + 1 != b:
        interest_lost += compute_interest(sol.slides[a].tags,sol.slides[a+1].tags)
        interest_lost += compute_interest(sol.slides[b-1].tags,sol.slides[b].tags)

        interest_gained += compute_interest(sol.slides[b].tags,sol.slides[a+1].tags)
        interest_gained += compute_interest(sol.slides[b-1].tags,sol.slides[a].tags)

        if a != 0:
            interest_lost += compute_interest(sol.slides[a-1].tags,sol.slides[a].tags)
            interest_gained += compute_interest(sol.slides[a-1].tags,sol.slides[b].tags)
        if b != (len(sol.slides)-1):
            interest_lost += compute_interest(sol.slides[b].tags,sol.slides[b+1].tags)
            interest_gained += compute_interest(sol.slides[a].tags,sol.slides[b+1].tags)
    elif a + 1 == b:
        if a != 0:
            interest_lost += compute_interest(sol.slides[a-1].tags,sol.slides[a].tags)
            interest_gained += compute_interest(sol.slides[a-1].tags,sol.slides[b].tags)
        if b != (len(sol.slides)-1):
            interest_lost += compute_interest(sol.slides[b].tags,sol.slides[b+1].tags)
            interest_gained += compute_interest(sol.slides[a].tags,sol.slides[b+1].tags)
    
    return sol.score + interest_gained - interest_lost


def rebuild_sol_from_blocks(blocks):
    sol = Solution([])
    for block in blocks:
        for slide in block:
            sol.add_slide(slide)
    return sol


def reorganise_blocks_tsp(blocks):
    # TSP entre blocs
    print(f'{len(blocks)} blocks')
    matrix = np.zeros((len(blocks), len(blocks)))
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            score = compute_interest(blocks[i][-1].tags, blocks[j][0].tags)
            if score:
                val = 100 / score
            else:
                val = 1000
            matrix[i, j] = val

    distance_matrix = np.array(matrix)
    distance_matrix[:, 0] = 0
    permutation, _ = solve_tsp_simulated_annealing(distance_matrix)

    return [blocks[i] for i in permutation]


def reorganise_greedy(blocks):
    res = [blocks.pop(0)]
    rd.shuffle(blocks)
    while blocks:
        if len(blocks) % 1000 == 0:
            print(f'reorganise greedy ... remaining {len(blocks)}')
        best_transition = -1
        best_block_id = 0
        for id, block in enumerate(blocks):
            # if id > 5000:
            #     break
            transition = max(compute_interest(res[-1][-1].tags, block[0].tags),
                                compute_interest(res[-1][-1].tags, block[-1].tags))
            if transition > best_transition:
            # if transition > 0:
                best_block_id = id
                # break  # TODO seulement pour b
                best_transition = transition
        best_block = blocks.pop(best_block_id)
        if compute_interest(res[-1][-1].tags, best_block[0].tags) > compute_interest(res[-1][-1].tags, block[-1].tags):
            res.append(best_block)
        else:
            res.append(best_block[::-1])
    return res


def break_under_thr(sol, threshold):
    blocks = []
    slides = deque(sol.slides)
    while slides:
        block = [slides.popleft()]
        for _ in range(len(slides)):
            if compute_interest(block[-1].tags, slides[0].tags) >= threshold:
                block.append(slides.popleft())
            else:
                break
        blocks.append(block)
    return blocks


def opti_block(sol, threshold=1):
    '''
    TODO decoupage par offset inferieur ou alea
    '''
    blocks = break_under_thr(sol, threshold)

    print('number of blocks :', len(blocks))
    # blocks = reorganise_blocks_tsp(blocks)
    blocks = reorganise_greedy(blocks)
    return rebuild_sol_from_blocks(blocks)
