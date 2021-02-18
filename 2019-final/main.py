import pickle
import sys
import random as rd
import pprint
import math
from copy import deepcopy
import itertools as it

from parser import parse, Solution, Data

from sn import compute_sn
from utils import compute_dependencies


MISC_DIR = '/home/seb/prog/hashcode/2019-final/misc/'
OUT_TEMPLATE =  MISC_DIR + 'solutions.template'


DATA_IN_FILE =  MISC_DIR + sys.argv[1]
OUT_FILE =      MISC_DIR + sys.argv[1] + '.out'


def compute_score(data, sol):
    # sol de type liste de tuple (file(str), server(int))
    score = 0
    serv_files = [set() for _ in range(data.servers_nb)]
    serv_times = [0] * data.servers_nb
    file_available_time = {}  # cle nom fichier, valeur temps à partir duquel il est dispo
    for file, serv in sol.steps:
        max_deb = 0
        for f in data.files[file].dependencies: # on verifie que les dépendances sont dispo
            if f not in serv_files[serv]:
                max_deb = max(max_deb, file_available_time[f])

        if max_deb > serv_times[serv]:
            serv_times[serv] = max_deb

        serv_files[serv].add(file)
        serv_times[serv] += data.files[file].compile_time
        file_available_time[file] = serv_times[serv] + data.files[file].replicate_time

        # si file est un fichier target, alors calcul du score
        if file in data.targets:
            if data.targets[file].deadline < serv_times[serv]:
                score += data.targets[file].points # goal points
                score += max(0, data.targets[file].deadline - serv_times[serv]) # speed points
            # else:
                # print('overtime :(')

    return score


def distribute(d:Data, files, res):
    seed = rd.randint(0, d.servers_nb - 1)
    # seed = 0
    for i, file in enumerate(sorted(files, key=lambda f: d.files[f].compile_time, reverse=True)):
        # res.append((file, rd.randint(0, d.servers_nb - 1)))
        res.append((file, (seed + i) % d.servers_nb))


def naive_greedy(d):
    s_n = compute_sn(d)
    placed = set()
    res = []
    for files in s_n[::-1]:
        distribute(d, files - placed, res)
        placed |= files
    return res


def greedy_by_target(d):
    res = []
    placed = set()
    # targets = sorted(d.targets.keys(), key= lambda t: d.targets[t].deadline)
    # targets = sorted(d.targets.keys(), key= lambda t: d.targets[t].points / d.targets[t].deadline, reverse=True)
    targets = list(d.targets.keys())
    rd.shuffle(targets)
    for target_name in targets:
        file = d.files[target_name]
        deps = compute_dependencies(file)
        for lvl in deps[::-1]:
            distribute(d, lvl - placed, res)
            placed |= lvl
        distribute(d, {target_name}, res)
    return res



if __name__ == '__main__':
    data = parse(DATA_IN_FILE)

    for name, file in data.files.items():
        print(f'{name} depends on {file.dependencies}')

    # print('parsing over')

    # scores = []
    # for _ in range(1):
    #     dc = deepcopy(data)
    #     # steps = naive_greedy(dc)
    #     steps = greedy_by_target(dc)
    #     score = compute_score(dc, Solution(len(steps), steps))
    #     print('score :', score)
    #     scores.append(score)
    # print('score max :', max(scores))

    # for file in data.files.values():
    #     print(f'{file.name} -> min time {file.min_time}, potential {file.potential}, heuristic {file.heuristic}')
  

    # with open('sol_' + sys.argv[1], 'rb') as f:
    #     sol = pickle.load(f)

    # with open('sol_' + sys.argv[1], 'wb') as f:
    #     pickle.dump(sol, f)