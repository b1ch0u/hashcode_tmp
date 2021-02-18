
import pickle
import sys

import random as rd
import pprint
import math
import itertools as it

from parser import parse

from simple import simple_solution

MISC_DIR = '/home/seb/prog/hashcode/2019-final/misc/'
OUT_TEMPLATE =  MISC_DIR + 'solutions.template'


DATA_IN_FILE =  MISC_DIR + sys.argv[1]
OUT_FILE =      MISC_DIR + sys.argv[1] + '.out'

def total_goalpts(d):
    sum=0
    for t in d.targets :
        sum+=t.points
    return sum


def compute_sn(data):
    sn=[[]]
    i=0
    sn[0]=set()
    fini = False
    for t in data.targets:
        sn[0].add(t)

    while(not fini):
        sn.append(set())
        fini = True
        for t in sn[i]:
            if (data.files[t].dependencies):
                fini = False
                sn[i+1]=sn[i+1] | set(data.files[t].dependencies) 
        i+=1

    sn.pop()
    return sn


def compute_score(data, sol):
    # sol de type liste de tuple (file(str), server(int))
    score = 0
    mem_serv = [[set(), 0] for _ in range(data.servers_nb)] # fichiers compilés dans chaque serv & donc indépendants de available time (en dessous) + temps pour chaque serveur 
    file_available_time = {}  # cle fichier, valeur temps à partir duquel il est dispo
    for s in sol.steps:
        max_deb = 0
        file, serv = s
        for f in data.files[file].dependencies: # on verifie que les dépendances sont dispo
            if f not in mem_serv[serv][0]:
                max_deb = max(max_deb, file_available_time[f])

        if max_deb > mem_serv[serv][1]:
            mem_serv[serv][1] = max_deb

        mem_serv[serv][0].add(s[0])
        mem_serv[serv][1] += data.files[file].compile_time
        file_available_time[s[0]] = mem_serv[s[1]][1] + data.files[s[0]].replicate_time

        # si s[0] est un fichier target, alors calcul du score
        if s[0] in data.targets:
            if data.targets[s[0]].deadline < mem_serv[s[1]][1]:
                score += data.targets[s[0]].points # goal points
                score += max(0, data.targets[s[0]].deadline - mem_serv[s[1]][1]) # speed points
            # else:
                # print('overtime :(')
    
    return score


if __name__ == '__main__':
    data = parse(DATA_IN_FILE)
    #print(data.targets)

    sol = simple_solution(data)
    print(compute_score(data, sol))
    #print(compute_sn(data))
    #print(sol)
