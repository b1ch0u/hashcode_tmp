import sys

import random as rd
import pprint
import math

import matplotlib.pyplot as plt

from jinja2 import Template

from ugp import parse_from_grammar

from parser import parse
from visu import visualize


MISC_DIR = '/home/seb/prog/hashcode/2016-qual/misc/'
# IN_GRAMMAR =    MISC_DIR + '2016.grammar'
# OUT_TEMPLATE =  MISC_DIR + 'solutions.template'

# DATA_IN_FILE =  MISC_DIR + 'busy_day.in'
# DATA_OUT_FILE = MISC_DIR + 'busy_day.out'

print(sys.argv[1])
DATA_IN_FILE = MISC_DIR + sys.argv[1]

# DATA_IN_FILE =  MISC_DIR + 'mother_of_all_warehouses.in'
# DATA_OUT_FILE = MISC_DIR + 'mother_of_all_warehouses.out'

# DATA_IN_FILE =  MISC_DIR + 'redundancy.in'
# DATA_OUT_FILE = MISC_DIR + 'redundancy.out'

# DATA_IN_FILE =  MISC_DIR + 'example.in'
# DATA_OUT_FILE = MISC_DIR + 'example.out'


def write_sol(data, sol, out_template_name, out_file_name):
    with open(out_template_name) as template_file, open(out_file_name, 'w') as out_file:
        template = Template(template_file.read())
        out_file.write(template.render(**data, sol=sol))


def check_validity(d, sol):
    pass


def compute_score(d, sol):
    pass


if __name__ == '__main__':
    # data = parse_from_grammar(DATA_IN_FILE, IN_GRAMMAR)
    data = parse(DATA_IN_FILE)
    # enrich_data(data)
    # print(data.keys())
    visualize(data, sys.argv[1])