import pickle
import sys

import random as rd
import pprint
import math
from collections import Counter, deque
import itertools as it

import matplotlib.pyplot as plt

from jinja2 import Template

from ugp import parse_from_grammar

from parser import parse

from matching import compute_matching_max
from utils import Solution, compute_interest
from graph import create_slides_horizontal_only, create_complete_graph, create_tsp_solution
from partition import extract_subgroup

from simple import greedy_solution, naive_vertical_slides, better_greedy

from opti import opti_permutation_slide, opti_block
# from visu import visualize


MISC_DIR = '/home/seb/prog/hashcode/2019-qual/misc/'
# IN_GRAMMAR =    MISC_DIR + '2016.grammar'
OUT_TEMPLATE =  MISC_DIR + 'solutions.template'
OUT_FILE =      MISC_DIR + sys.argv[1] + '.out'


DATA_IN_FILE = MISC_DIR + sys.argv[1]


def write_sol(data, sol, out_template_name, out_file_name):
    with open(out_template_name) as template_file, open(out_file_name, 'w') as out_file:
        template = Template(template_file.read())
        out_file.write(template.render(**data, sol=sol))


def compute_avg_score(slides, N=10):
    scores = []
    for i in range(N):
        print(f'in compute_avg_score : {i} / {N}')
        current_slide = rd.choice(slides)
        for slide in slides:
            score = compute_interest(current_slide.tags, slide.tags)
            if score:
                scores.append(score)
    avg = sum(scores) / len(scores)
    plt.hist(scores)
    plt.title(DATA_IN_FILE)
    plt.show()
    return avg


def reorganise_slides(slides, offset, max_dist=500):
    res = deque()
    slides = deque(slides)
    while slides:
        if len(slides) % 100 == 0:
            print(f'reorganizing ... remaining {len(slides)}')
        current_slide = slides.popleft()
        res.append(current_slide)
        for _ in range(min(max_dist, len(slides))):
            if compute_interest(slides[0].tags, current_slide.tags) >= offset:
                res.append(slides.popleft())
            else:
                slides.rotate(-1)
    return res


def push_sol(data, sol, current_best_score):
    if sol.score > current_best_score:
        write_sol(data, sol, OUT_TEMPLATE, OUT_FILE)
    


if __name__ == '__main__':
    # data = parse(DATA_IN_FILE)

    # slides = naive_vertical_slides(data, 100)


    # avg_positive_score = compute_avg_score(slides)
    # min_selection_score = int(input('enter offset : '))
    # min_selection_score = 2

    # slides = reorganise_slides(slides, min_selection_score)
    # for _ in range(10):
    #     slides = reorganise_slides(slides, min_selection_score)
    #     sol = Solution([])
    #     for slide in slides:
    #         sol.add_slide(slide)
    #     print('score :', sol.score)
    #     id = rd.randint(1, len(slides) - 1)
    #     slides.rotate(id)

    # gs = 100
    # sol = Solution([])
    # for i in range(len(slides) // gs):
    #     subslides = slides[gs * i: gs + gs * i]
    #     perm, score = create_tsp_solution(subslides)
    #     for id in perm:
    #         sol.add_slide(subslides[id])
    #     print('current score', sol.score)
    # exit()

    # print('max points :', sum(int(len(slide.tags) / 2) for slide in slides))
    # exit()

    # tags_count = Counter()
    # for slide in slides:
    #     tags_count.update(slide.tags)
    # print('number of different tags', len(tags_count))
    # print('most common tags', tags_count.most_common(3))
    
    # scores = []
    # first_slide = slides[0]
    # m = 0
    # for i, s1 in enumerate(slides[:1000]):
    #     m = max(m, max(compute_interest(s1.tags, s2.tags)
    #                     for s2 in slides[i + 1:]))
    # print('m', m)

    # for slide in slides[1:]:
    #     score = compute_interest(first_slide.tags, slide.tags)
    #     if score:
    #         scores.append(score)
    # print('number of non null scores', len(scores))
    # plt.hist(scores)
    # plt.show()
    # exit()

    # greedy_depth = int(input('enter greedy depth : '))
    # sol = greedy_solution(slides, greedy_depth)

    # sol = better_greedy(slides)

    # with open('sol_' + sys.argv[1], 'wb') as f:
    #     pickle.dump(sol, f)

    # with open('sol_' + sys.argv[1], 'rb') as f:
    with open('sol_b_opti', 'rb') as f:
        sol = pickle.load(f)

    print('score avant opti', sol.score)
    current_score = sol.score

    if current_score > 382129:
        print('writing')
        with open('sol_' + sys.argv[1] + '2', 'wb') as f:
            pickle.dump(sol, f)


    scores = [compute_interest(s1.tags, s2.tags) for s1, s2 in zip(sol.slides, sol.slides[1:])]
    print('set of scores', set(scores))
    plt.hist(scores)
    plt.title('transition scores')
    plt.show()
    # thr = int(input('enter threshold : '))
    thr = 1
    for _ in range(10):
        sol = opti_block(sol, thr)
        print('score apres opti', sol.score)
        # TODO fonction push_solution gere un pool, affiche le score, garde eventuellement histo, etc
        if sol.score <= current_score:
        #     thr += 1
            print(f'increasing threashold to {thr}')
        else:
            print('writing new best sol')
            with open('sol_' + sys.argv[1] + '2', 'wb') as f:
                pickle.dump(sol, f)
        current_score = sol.score # TODO new_sol vs sol