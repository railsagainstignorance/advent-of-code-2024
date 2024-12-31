import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
import pprint

from utils import *

instances = [
    {
        'input': '''\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb''',
    'num_possible_designs': 6,
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'num_possible_designs',
    ]

def solve( instance ):

    def parse_input( input ):
        strs = get_array_of_strings_from_input( input )
        towels = strs.pop(0).split(', ')
        strs.pop(0)
        designs = strs

        towel_options = '|'.join(towels)
        design_re_str = f"^(?:{towel_options})+$"
        design_prog = re.compile(design_re_str)

        return towels, designs, design_prog

    towels, designs, design_prog = parse_input( instance['input'] )
    # print(f"DEBUG: towels={towels}, designs={designs}")

    def assess_designs( designs, design_prog ):
        num_achievable_designs = 0
        for design in designs:
            m = design_prog.match( design )
            if m:
                num_achievable_designs += 1

        return num_achievable_designs

    num_possible_designs = assess_designs( designs, design_prog )

    return {
        'num_possible_designs': num_possible_designs,
        }

def run():
    print_here()
    verbose = True
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    if verbose:
        pprint.pp( response )
    else:
        print( response )

if __name__ == "__main__":
    run()

# [{'elapsed_time_s': 8.750008419156075e-05},
#  {'num_possible_designs': 342, 'elapsed_time_s': 0.0073116670828312635}]