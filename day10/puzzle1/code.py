import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
0123
1234
8765
9876''',
        'trailhead_scores': [1],
        'sum_trailhead_scores': 1,
    },
    {
        'input': '''\
1110111
1111111
1112111
6543456
7111117
8111118
9111119''',
        'trailhead_scores': [2],
        'sum_trailhead_scores': 2,
    },
    {
        'input': '''\
1190119
1111198
1112117
6543456
7651987
8761111
9871111''',
        'trailhead_scores': [4],
        'sum_trailhead_scores': 4,
    },
    {
        'input': '''\
1011911
2111811
3111711
4567654
1118113
1119112
1111101''',
        'trailhead_scores': [1,2],
        'sum_trailhead_scores': 3,
    },
    {
        'input': '''\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732''',
        'trailhead_scores': [5, 6, 5, 3, 1, 3, 5, 3,5],
        'sum_trailhead_scores': 36,
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'trailhead_scores',
    'sum_trailhead_scores'
    ]

def solve( case ):

    int_yx_array = get_int_yx_array_from_input( case['input'] ) 
    max_y = len(int_yx_array)
    min_y = 0
    max_x = len(int_yx_array[0])
    min_x = 0

    # find all trailheads
    trailhead_coords = []
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if int_yx_array[y][x] == 0:
                trailhead_coords.append( (x, y) )

    def find_trails_to_9s( x, y, known_9_coords_set: set):
        if int_yx_array[y][x] == 9:
            known_9_coords_set.add( (x, y) )
            return
        height = int_yx_array[y][x]
        for direction in range(4):
            dx, dy = coord_delta_by_direction[direction]
            new_x = x + dx
            new_y = y + dy
            if new_x >= min_x and new_x < max_x and new_y >= min_y and new_y < max_y:
                new_height = int_yx_array[new_y][new_x]
                if new_height == height +1:
                    find_trails_to_9s( new_x, new_y, known_9_coords_set )

    trailhead_scores = []

    for trailhead_coord in trailhead_coords:
        x, y = trailhead_coord
        known_9_coords_set = set()
        find_trails_to_9s( x, y, known_9_coords_set )
        trailhead_scores.append( len(known_9_coords_set) )

    sum_trailhead_scores = sum(trailhead_scores)

    return {
        'trailhead_scores': trailhead_scores,
        'sum_trailhead_scores': sum_trailhead_scores
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

