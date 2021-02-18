import random as rd
import pprint
import math

import matplotlib.pyplot as plt

from jinja2 import Template

from ugp import parse_from_grammar

from assign import *
from enrich import enrich_data
from pl import *
from rd import *
from opti import assign_server_from_max_to_min_guar_cap
from solution import Solution
from mcts import mcts_find_best_child, mcts_explore
from node import Node


MISC_DIR = '/home/seb/prog/hashcode/2015-qual/misc/'
IN_GRAMMAR =    MISC_DIR + '2015.grammar'
OUT_TEMPLATE =  MISC_DIR + 'solutions.template'

DATA_IN_FILE =  MISC_DIR + 'dc.in'
DATA_OUT_FILE = MISC_DIR + 'dc.out'

# DATA_IN_FILE =  MISC_DIR + 'example.in'
# DATA_OUT_FILE = MISC_DIR + 'example.out'


def write_sol(data, sol, out_template_name, out_file_name):
    with open(out_template_name) as template_file, open(out_file_name, 'w') as out_file:
        template = Template(template_file.read())
        out_file.write(template.render(**data, sol=sol))


def check_validity(d, sol):
    rows_content, pools_content = sol

    # verifier les blocks
    assert len(rows_content) == d['rows_nb']


    # chaque serv n'est assigne qu'a une ligne
    for serv_nb in range(d['servers_nb']):
        try:
            assert sum((serv_nb in row)
                        for row in rows_content) <= 1
        except:
            print(f'PROBLEM with server {serv_nb} assigned to multiple rows')

    # chaque serv n'est assigne qu'a un pool
    for serv_nb in range(d['servers_nb']):
        try:
            assert sum((serv_nb in pool)
                        for pool in pools_content) <= 1
        except:
            print(f'PROBLEM with server {serv_nb} assigned to multiple pools')

    return True


def compute_score(d, sol):
    rows_content, pools_content = sol

    servers_row = [None] * d['servers_nb']
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
    return min(gcs)


def old_main(data, rows_content, pools_content):
    # print('rows', rows_content)
    # print('pools', pools_content)

    print('score :', compute_score(data, (rows_content, pools_content)))

    for _ in range(50):
        print(f'{_}')
        print('intelligente')
        best_score, best_sol = rd_improve_sol(
                        data,
                        10000,
                        rows_content,
                        pools_content,
                        compute_score,
                        assign_server_from_max_to_min_guar_cap)
        rows_content, pools_content = best_sol

        print('naive')
        best_score, best_sol = rd_improve_sol(
                        data,
                        1000,
                        rows_content,
                        pools_content,
                        compute_score,
                        randomly_change_one_assignation)
        rows_content, pools_content = best_sol

    print('best rows content:', rows_content)
    print('best pools content:', pools_content)
    print('best score:', compute_score(data, best_sol))
    print('validity:', check_validity(data, best_sol))


if __name__ == '__main__':
    data = parse_from_grammar(DATA_IN_FILE, IN_GRAMMAR)
    enrich_data(data)

    # coeff = 1.07
    # rows_content = pl_assign(data, coeff)

    rows_content = [[33, 134, 249, 65, 88, 129, 225, 264, 283, 307, 341, 498, 596, 314, 274, 541, 13, 101, 215, 241, 243, 354, 374, 18, 359, 456, 500, 586, 603, 613], [448, 458, 461, 479, 553, 566, 572, 594, 221, 302, 452, 387, 464, 114, 28, 164, 17, 45, 84, 128, 169, 190, 216, 219, 246, 336, 340, 578], [43, 46, 76, 141, 159, 170, 282, 356, 358, 363, 397, 426, 475, 571, 584, 7, 244, 383, 565, 83, 236, 310, 25, 51, 103, 150, 194, 238, 342, 434, 454, 502, 539, 542, 622], [49, 50, 381, 420, 466, 165, 228, 325, 357, 208, 419, 429, 583, 240, 131, 191, 556, 592, 615, 457, 23, 179, 421, 465, 523, 525, 171, 529], [90, 330, 518, 520, 609, 607, 34, 145, 352, 52, 210, 63, 95, 200, 206, 293, 328, 353, 481, 510, 540, 560, 91, 94, 126, 161, 185, 197, 254, 281, 289, 326, 362, 396, 433, 443, 463, 504, 505, 522, 526, 559, 569], [136, 368, 487, 8, 139, 204, 232, 295, 298, 337, 350, 530, 173, 414, 19, 100, 132, 147, 280, 312, 313, 318, 389, 430, 483, 501, 574, 66, 267, 605, 40, 373], [320, 77, 113, 120, 146, 273, 360, 405, 431, 59, 149, 163, 260, 335, 361, 377, 379, 422, 455, 488, 62, 193, 201, 248, 399, 415, 554], [14, 44, 56, 86, 160, 198, 305, 486, 514, 535, 601, 11, 20, 24, 48, 60, 89, 99, 122, 309, 315, 324, 369, 386, 404, 438, 469, 624], [79, 331, 38, 67, 82, 220, 265, 304, 321, 384, 477, 480, 485, 576, 602, 133, 408, 489, 492, 528, 580, 58, 233, 296, 329, 334, 538, 507, 612, 64, 432, 552], [106, 205, 245, 253, 268, 290, 394, 591, 119, 135, 262, 428, 445, 57, 382, 416, 545, 587, 606, 123, 598, 29, 409, 513, 519, 229, 497, 532], [124, 436, 549, 610, 61, 297, 5, 30, 202, 239, 1, 286, 15, 32, 78, 107, 148, 151, 157, 178, 269, 299, 367, 370, 515, 608, 125, 279, 412, 427, 0, 562], [351, 371, 376, 453, 499, 600, 339, 346, 410, 621, 54, 75, 98, 110, 112, 140, 155, 209, 231, 266, 355, 375, 378, 474, 508, 517, 16, 292, 558, 31, 127, 217, 548, 570], [10, 180, 182, 222, 327, 344, 407, 503, 521, 536, 585, 72, 80, 142, 153, 154, 187, 195, 338, 451, 524, 527, 561, 597, 611, 619, 285, 2, 116, 69, 291, 496], [117, 181, 184, 199, 440, 444, 531, 37, 172, 252, 380, 401, 406, 188, 537, 70, 109, 247, 306, 511, 144, 207, 470, 512, 567], [196, 105, 203, 256, 347, 349, 435, 484, 573, 41, 102, 158, 183, 271, 294, 333, 411, 446, 493, 81, 261, 322, 332, 366, 403, 423, 494, 234], [93, 226, 278, 251, 348, 418, 439, 460, 575, 168, 257, 316, 392, 495, 557, 623, 92, 176, 250, 308, 364, 588, 35, 137, 275, 390, 417, 509]]
    pools_content = [[508, 418, 498, 120, 356, 148, 216, 601, 196, 254, 484, 403], [433, 67, 332, 172, 35, 107, 517, 267, 116, 243], [586, 265, 286, 377, 434, 624, 538, 260, 578, 479], [168, 123, 16, 562, 180, 548, 79, 236, 389], [82, 456, 63, 207, 610, 257, 206, 60, 420], [435, 383, 182, 500, 239, 592, 414, 28, 526, 86], [310, 430, 327, 374, 505, 70, 19, 308, 427], [136, 470, 163, 312, 245, 297, 404, 460, 234, 229, 341, 298, 190, 552, 75], [179, 354, 558, 561, 99, 59, 622, 5], [607, 292, 566, 176, 521, 158, 535, 210, 488, 496], [225, 217, 90, 325, 392, 380, 54, 469, 448, 585], [518, 302, 509, 1, 316, 342, 278, 268, 428, 455, 199, 454, 273], [280, 183, 436, 489, 511, 594, 142, 248, 409, 124], [541, 411, 78, 501, 386, 95, 611, 50, 313, 495, 474], [431, 376, 290, 397, 615, 281, 588, 275, 528, 76, 198, 69, 529], [244, 540, 333, 580, 503, 232, 247, 422, 446, 363, 122], [14, 188, 145, 602, 246, 463, 91, 110, 605, 527], [24, 358, 193, 154, 305, 416, 240, 197, 399], [322, 146, 480, 417, 621, 219, 379, 221, 560, 444, 127], [38, 384, 360, 266, 353, 40, 187, 569, 407, 170, 150, 151, 58, 37, 587], [485, 423, 165, 220, 109, 378, 536, 114, 554], [262, 140, 439, 112, 228, 350, 31, 515, 204, 249, 131, 307], [606, 443, 18, 173, 101, 396, 512, 483, 318, 531, 571, 487, 348], [23, 337, 83, 553, 105, 33, 88, 497, 293, 62], [274, 596, 619, 549, 461, 574, 373, 119, 251], [157, 279, 486, 432, 72, 141, 49, 134, 466, 368, 366, 233, 504, 539], [492, 135, 346, 340, 113, 178, 2, 494, 32], [355, 10, 56, 52, 477, 81, 106, 256, 250, 15], [570, 352, 184, 493, 43, 84, 205, 315, 612, 0, 545], [80, 195, 338, 155, 576, 387, 457, 202, 208, 7, 408, 565], [451, 181, 215, 370, 405, 523, 426, 48, 126, 98, 226, 45, 481], [299, 294, 608, 282, 575, 344, 598, 465, 94, 321], [361, 583, 452, 20, 375, 296, 499, 329, 572, 429, 147, 502], [89, 573, 357, 359, 351, 347, 532, 271, 609, 603], [201, 46, 161, 530, 381, 117, 285, 103, 253, 510, 556], [41, 194, 475, 222, 100, 65, 522, 264, 542, 44, 369, 128], [336, 382, 252, 584, 93, 326, 335, 153, 524, 406, 200], [364, 390, 330, 519, 331, 61, 324, 349, 291, 34, 209, 125, 129], [238, 102, 412, 458, 133, 591, 567, 362, 328], [613, 421, 144, 371, 66, 557, 597, 559, 438], [139, 241, 320, 314, 17, 231, 600, 339, 164, 289, 513, 537, 160], [514, 410, 171, 295, 304, 367, 51, 159, 13, 445, 453, 137], [185, 419, 57, 306, 169, 25, 30, 92, 283, 507, 29], [394, 401, 520, 261, 8, 623, 77, 269, 191, 415], [64, 440, 149, 203, 132, 334, 309, 464, 525, 11]]

    sol = Node(Solution(data, rows_content, pools=pools_content))
    print('current score:', sol.state.score)

    # mcts_explore(sol, 500, 10)
    # exit()

    best_sol = sol

    unsuccesful_tries = 1
    for _ in range(400):
        # print(sol.pools)
        print('one try')
        improved_sol = mcts_find_best_child(sol, 200)
        # assert sol.state.pools != improved_sol.state.pools
        # print(improved_sol.state.pools)

        if improved_sol.state.score >= sol.state.score or unsuccesful_tries == 5:
            if improved_sol.state.score > best_sol.state.score:
                best_sol = sol
            print('new score:', improved_sol.state.score)
            pools = improved_sol.state.pools
            sol = Node(Solution(data, rows_content, pools))
            unsuccesful_tries = 0
        else:
            pools = sol.state.pools
            sol = Node(Solution(data, rows_content, pools))
            unsuccesful_tries += 1
        # print()
        # print()
        # print(sol.children)
    # print(sol.state.rows)
    # print(sol.state.pools)

    print(rows_content)
    print(best_sol.state.pools)
    print('score', best_sol.state.score)