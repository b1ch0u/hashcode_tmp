import itertools as it

import networkx as nx


def total_affinity(s1, s2):
    return len(s1 | s2)


def percentage_affinity(s1, s2):
    return 1 - (len(s1) + len(s2)) / len(s1 | s2)


def compute_matching_max(photos_V, affinity_func):
    G = nx.Graph()

    G.add_nodes_from([photo.id for photo in photos_V])

    edges = []
    for p1, p2 in it.combinations(photos_V, 2):
        score = affinity_func(p1.tags, p2.tags)
        edges.append((p1.id, p2.id, score))

    G.add_weighted_edges_from(edges)

    return nx.max_weight_matching(G)