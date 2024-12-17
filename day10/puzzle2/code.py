import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
8888808
8843218
8858828
8865438
1171141
1187651
1191111''',
        'trailhead_scores': [1],
        'sum_trailhead_scores': 1,
        'trailhead_ratings': [3],
        'sum_trailhead_ratings': 3,
    },
    {
        'input': '''\
012345
123456
234567
345678
416789
567891''',
        'trailhead_scores': [2],
        'sum_trailhead_scores': 2,
        'trailhead_ratings': [121+106],
        'sum_trailhead_ratings': 227,
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
        'trailhead_ratings': [20, 24, 10, 4, 1, 4, 5, 8, 5],
        'sum_trailhead_ratings': 81,
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'trailhead_scores',
    'sum_trailhead_scores',
    'trailhead_ratings',
    'sum_trailhead_ratings',
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

    def find_trails_to_9s( x, y, trail_counts_by_destination_coord: dict[str, int] ):
        if int_yx_array[y][x] == 9:
            destination_coord = (x, y)
            if not destination_coord in trail_counts_by_destination_coord:
                trail_counts_by_destination_coord[destination_coord] = 0
            trail_counts_by_destination_coord[destination_coord] += 1
            return
        height = int_yx_array[y][x]
        for direction in range(4):
            dx, dy = coord_delta_by_direction[direction]
            new_x = x + dx
            new_y = y + dy
            if new_x >= min_x and new_x < max_x and new_y >= min_y and new_y < max_y:
                new_height = int_yx_array[new_y][new_x]
                if new_height == height +1:
                    find_trails_to_9s( new_x, new_y, trail_counts_by_destination_coord )

    trailhead_scores = []
    trailhead_ratings = []

    for trailhead_coord in trailhead_coords:
        x, y = trailhead_coord
        trail_counts_by_destination_coord = {}
        find_trails_to_9s( x, y, trail_counts_by_destination_coord )
        trailhead_scores.append( len(trail_counts_by_destination_coord) )
        trailhead_ratings.append( sum(trail_counts_by_destination_coord.values()) )

    sum_trailhead_scores = sum(trailhead_scores)
    sum_trailhead_ratings = sum(trailhead_ratings)

    return {
        'trailhead_scores': trailhead_scores,
        'sum_trailhead_scores': sum_trailhead_scores,
        'trailhead_ratings': trailhead_ratings,
        'sum_trailhead_ratings': sum_trailhead_ratings,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-17: day10/puzzle2/..
# [{'sum_trailhead_ratings': 1186, 'elapsed_time_s': 0.002405292121693492}]