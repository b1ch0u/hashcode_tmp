import random as rd
import math

import matplotlib.pyplot as plt

from jinja2 import Template

from ugp import parse_from_grammar

MISC_DIR = '/home/seb/prog/hashcode/2014/misc/'
DATA_IN_FILE =  MISC_DIR + 'paris.in'
IN_GRAMMAR =    MISC_DIR + '2014.grammar'
OUT_TEMPLATE =  MISC_DIR + 'solutions.template'
DATA_OUT_FILE = MISC_DIR + 'paris.out'

# DATA_IN_FILE =  MISC_DIR + 'example.in'
# IN_GRAMMAR =    MISC_DIR + '2014.grammar'
# OUT_TEMPLATE =  MISC_DIR + 'solutions.template'
# DATA_OUT_FILE = MISC_DIR + 'example.out'

def write_sol(data, sol, out_template_name, out_file_name):
    with open(out_template_name) as template_file, open(out_file_name, 'w') as out_file:
        template = Template(template_file.read())
        out_file.write(template.render(**data, sol=sol))


def enrich_data(data):
    for node in data['nodes']:
        node['children'] = {}
    data['costs'] = {}
    for street in data['streets']:
        data['nodes'][street['start']]['children'][street['end']] = street
        data['costs'][(street['start'], street['end'])] = street['cost']
        if street['type'] == 2:
            other_way = street.copy()
            other_way['start'], other_way['end'] = other_way['end'], other_way['start']
            data['nodes'][street['end']]['children'][street['start']] = other_way
            data['costs'][(street['end'], street['start'])] = street['cost']


def create_solution_vertical(data):
    sol = [[data['initial_node']] for _ in range(data['cars_nb'])]
    visited = set()
    score = 0
    for car in range(data['cars_nb']):
        total_time = 0
        current_node = data['initial_node']
        while total_time < data['max_time']:
            possible_streets = list(data['nodes'][current_node]['children'].values())
            if any((current_node, street['end']) not in visited for street in possible_streets):
                possible_streets = [street for street in possible_streets
                                    if (current_node, street['end']) not in visited]
            weights = [street['value'] / street['cost']
                       for street in possible_streets]
            chosen_street = rd.choices(possible_streets, weights=weights)[0]
            total_time += chosen_street['cost']
            if total_time < data['max_time']:
                sol[car].append(chosen_street['end'])
                if (current_node, chosen_street['end']) not in visited:
                    score += chosen_street['value']
                    visited.add((current_node, chosen_street['end']))
                    visited.add((chosen_street['end'], current_node))
            current_node = chosen_street['end']
    return {'paths': sol, 'score': score, 'cars_not_finished': set()}


def create_solution_horizontal(data):
    sol = [[data['initial_node']] for _ in range(data['cars_nb'])]
    visited = set()
    score = 0
    cars_not_finished = list(range(data['cars_nb']))
    cars_total_time = [0 for _ in range(data['cars_nb'])]
    while cars_not_finished:
        car = rd.choice(cars_not_finished)
        current_node = sol[car][-1]
        possible_streets = list(data['nodes'][current_node]['children'].values())
        if any((current_node, street['end']) not in visited
                for street in possible_streets):
            possible_streets = [street for street in possible_streets
                                if (current_node, street['end']) not in visited]
            weights = [street['value'] / street['cost']
                        for street in possible_streets]
        else:
            weights = [1 / street['cost'] for street in possible_streets]
        chosen_street = rd.choices(possible_streets, weights=weights)[0]
        cars_total_time[car] += chosen_street['cost']
        if cars_total_time[car] < data['max_time']:
            sol[car].append(chosen_street['end'])
            if (current_node, chosen_street['end']) not in visited:
                score += chosen_street['value']
                visited.add((current_node, chosen_street['end']))
                visited.add((chosen_street['end'], current_node))
        else:
            cars_not_finished.remove(car)
    return {'paths': sol, 'score': score, 'cars_not_finished': set()}


def check_validity(data, sol):
    for itinerary in sol['paths']:
        total_cost = 0
        for start, end in zip(itinerary, itinerary[1:]):
            if end not in data['nodes'][start]['children']:
                print('no continuity')
                return False
            total_cost += data['nodes'][start]['children'][end]['cost']
        if total_cost > data['max_time']:
            print('above total time')
            return False
    return True


def compute_score(data, sol):
    res = 0
    already_vivisted = set()
    for itinerary in sol:
        for start, end in zip(itinerary, itinerary[1:]):
            if (start, end) not in already_vivisted:
                res += data['nodes'][start]['children'][end]['value']
                already_vivisted.add((start, end))
                already_vivisted.add((end, start))
    return res


def instanciate_sol(data):
    return {
        'cars_not_finished': set(range(8)),
        'paths': [[data['initial_node']] for _ in range(8)],
        'best_path': [],
        'paths_cost': [0] * 8,
        'visited': set(),
        'score': 0
    }


# def bruteforce(graph, start_node):
#     pass


# def greedy_lookahead(d, sol, depth, sub_sol=None):  # TODO ajouter score suffisant pour arrêter recherche
#     if depth == 0:
#         return 0, None
#     if sub_sol is None:
#         sub_sol = instanciate_sol(d)
#     car = rd.choice(tuple(sol['cars_not_finished']))
#     pos = sol['paths'][car][-1]
#     current_cost = sub_sol['paths_cost'][car]
#     node = d['nodes'][pos]
#     children = node['children'].keys()
#     children = [child for child in children
#                 if current_cost + d['costs'][(pos, child)] < d['max_time']]
#     best_value = -1
#     for child in children:
#         added_value = node['children'][child]['value'] \
#             if ((pos, child) not in current_solution
#                 and (child, pos) not in current_solution
#                 and (pos, child) not in sol['visited']
#                 and (child, pos) not in sol['visited']) \
#             else 0
#         best_path.append((pos, child))
#         sub_value = greedy_lookahead(d, sol, depth - 1, best_path)
#         best_path.pop(-1)
#         if added_value > best_value:
#             best_value = added_value
#             best_child = child
    # else:
    #     graph = create_tmp_neigh_graph(data, pos, depth)


def best_random_solution(data, N, create_function, check_function, score_function):
    best_score = 0
    scores = []
    plt.ion()
    plt.show()
    for i in range(1, N + 1):
        if i % 10 == 0:
            print(f'iteration {i}')
            plt.clf()
            plt.hist(scores, bins=min(len(scores), 25))
            plt.draw()
            plt.pause(0.001)
        sol = create_function(data)
        score = sol['score']
        scores.append(sol['score'])
        # assert check_validity(data, sol)
        if score > best_score:
            best_score = score
            best_sol = sol
            print(f'best score: {best_score:,}')
    plt.ioff()
    plt.clf()
    plt.hist(scores, bins = 25)
    plt.title('final histogram')
    plt.show()
    print('avg', sum(scores) / len(scores))
    return best_score, best_sol


if __name__ == '__main__':
    data = parse_from_grammar(DATA_IN_FILE, IN_GRAMMAR)
    enrich_data(data)
    # print(sum(street['cost'] for street in data['streets']))
    # print(data['cars_nb'], data['max_time'])
    # print(sum(street['value'] for street in data['streets']))
    # costs = [street['cost'] for street in data['streets']]
    # values = [street['value'] for street in data['streets']]
    # plt.scatter(costs, values)
    # plt.show()
    # exit()

    # score, sol = best_random_solution(data, 200,
    #                                   create_solution_vertical, check_validity, compute_score)

    score, sol = best_random_solution(data, 1000,
                                      create_solution_horizontal, check_validity, compute_score)
    
    print(f'score: {score:,}')
    write_sol(data, sol, OUT_TEMPLATE, DATA_OUT_FILE)

    # TODO ajouter multiprocessing
    # TODO partitioner graphe