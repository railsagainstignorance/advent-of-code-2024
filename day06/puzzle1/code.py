import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...''',
        'initial_guard_xy': (4,6),
        'num_distinct_visited_positions': 41
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'initial_guard_xy',
    'num_distinct_visited_positions', 
    ]

def solve( case ):
    char_yx_array = get_char_yx_array_from_input( case['input'] )

    max_x = len(char_yx_array[0])
    max_y = len(char_yx_array)
    min_x = 0
    min_y = 0

    initial_guard_char = '^'
    initial_guard_direction = 3 # n
    obstacle_char = '#'
    path_char = 'X'

    guard_direction_chars = ['>', 'v', '<', '^']

    # locate initial coord of guard
    guard_y = None
    guard_x = None
    for y, row in enumerate(char_yx_array):
        if initial_guard_char in row:
            guard_y = y
            guard_x = row.index(initial_guard_char)
            break

    # iterate guard's path

    x = guard_x
    y = guard_y
    direction = initial_guard_direction

    char_yx_array[guard_y][guard_x] = path_char
    num_distinct_visited_positions = 1

    while True:
        coord_delta = coord_delta_by_direction[direction]
        next_x = x + coord_delta[0]
        next_y = y + coord_delta[1]

        if next_x < min_x or next_x >= max_x or next_y < min_y or next_y >= max_y:
            break

        if char_yx_array[next_y][next_x] == obstacle_char:
            direction = (direction + 1) % 4
        else:   
            x = next_x
            y = next_y
            if char_yx_array[y][x] != path_char:
                char_yx_array[y][x] = path_char
                num_distinct_visited_positions += 1
    
    return {
        'initial_guard_xy': (guard_x, guard_y),
        'num_distinct_visited_positions': num_distinct_visited_positions
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-16: day06/puzzle1/..
# [{'num_distinct_visited_positions': 4939}]