import itertools as it

from utils import compute_interest, Slide

import numpy as np
from python_tsp.heuristics import solve_tsp_simulated_annealing

def create_slides_horizontal_only(data):
    slides = []
    for photo in data.photos:
        if photo.orientation == 'H':
            slides.append(Slide.from_H_photo(photo))
    return slides


def create_complete_graph(slides):
    G = nx.Graph()

    G.add_nodes_from(range(len(slides)))

    edges = []
    for i, j in it.combinations(range(len(slides)), 2):
        edges.append(-compute_interest(slides[i].tags, slides[j].tags))

    G.add_weighted_edges_from(edges)

    return G


def create_tsp_solution(slides):
    if not slides:
        return
    matrix = np.zeros((len(slides), len(slides)))
    for i, j in it.combinations(range(len(slides)), 2):
        score = compute_interest(slides[i].tags, slides[j].tags)
        if score:
            val = 100 / score
        else:
            val = 1000
        matrix[i, j] = val
        matrix[j, i] = val

    distance_matrix = np.array(matrix)
    distance_matrix[:, 0] = 0
    permutation, score = solve_tsp_simulated_annealing(distance_matrix)

    return permutation, score