import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
import pprint

import networkx as nx
import matplotlib.pyplot as plt

from utils import *

instances = [
    {        
        'input': '''\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####''',
        'locks_heights': [
            [0,5,3,4,3],
            [1,2,0,5,3]
        ],
        'keys_heights': [
            [5,0,2,1,3],
            [4,3,4,0,2],
            [3,0,2,0,1]
        ],
        'num_unique_lock_key_pairs': 3, 
    }, 
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'locks_heights',
    'keys_heights',
    'num_unique_lock_key_pairs'
    ]

def solve( instance ):

    def parse_input( input ):
        # "So, you could say the first lock has pin heights 0,5,3,4,3:"

        # #####
        # .####
        # .####
        # .####
        # .#.#.
        # .#...
        # .....

        # "Or, that the first key has heights 5,0,2,1,3:"

        # .....
        # #....
        # #....
        # #...#
        # #.#.#
        # #.###
        # #####

        locks_heights = []
        keys_heights = []

        lines = get_array_of_strings_from_input( input )
        heights = None
        num_rows = None
        for line in lines:
            if line == '':
                continue
            elif len(line) != 5:
                raise Exception( f'unexpected line={line}' )
        
            if heights == None:
                num_rows = 0
                heights = [0,0,0,0,0]
            elif num_rows == 5:
                if line == '#####': # final row is # => key => 5-dots = height
                    keys_heights.append( heights )
                elif line == '.....': # final row is . => lock => 5-dots = height
                    locks_heights.append( heights )
                else:
                    raise Exception(f"unexpected line={line}")

                heights = None
                num_rows = None
            else:
                num_rows += 1
                for i in range(0,5):
                    if line[i]=='#':
                        heights[i] += 1

        return locks_heights, keys_heights

    def count_non_overlapping_lock_key_pairs( locks_heights, keys_heights ):
        num_unique_lock_key_pairs = 0

        for lock_heights in locks_heights:
            for key_heights in keys_heights:
                overlap = False
                for i in range(0,5):
                    if lock_heights[i] + key_heights[i] > 5:
                        overlap = True
                        break
                if not overlap:
                    num_unique_lock_key_pairs += 1

        return num_unique_lock_key_pairs

    #--- eof defs

    locks_heights, keys_heights = parse_input( instance['input'] )
    num_unique_lock_key_pairs = count_non_overlapping_lock_key_pairs( locks_heights, keys_heights )

    return {
        'locks_heights': locks_heights,
        'keys_heights': keys_heights,
        'num_unique_lock_key_pairs': num_unique_lock_key_pairs
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    if verbose:
        pprint.pp( response )
    else:
        print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2025-01-13: day25/puzzle1/..
# [{'elapsed_time_s': 2.02918890863657e-05}, {'num_unique_lock_key_pairs': 3077, 'elapsed_time_s': 0.00860029086470604}]