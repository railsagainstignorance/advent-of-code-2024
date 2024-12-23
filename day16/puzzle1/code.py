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
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############''',
    'best_path_score': 7036,
    },
    {
        'input': '''\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################''',
    'best_path_score': 11048,
    },
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'best_path_score',
    ]

def solve( instance ):

    def parse_input( input ):
        strs = get_array_of_strings_from_input( input )
        char_2d_array = [ list(row_str) for row_str in strs ]
        s_coord = None
        e_coord = None
        for y, row in enumerate(char_2d_array):
            for x, char in enumerate(row):
                if char == 'S':
                    s_coord = (x, y)
                if char == 'E':
                    e_coord = (x, y)

        return char_2d_array, s_coord, e_coord

    char_2d_array, s_coord, e_coord = parse_input( instance['input'] )

    def get_best_path_score( char_2d_array, s_coord, e_coord ):
        initial_direction = 0
        initial_score = 0
        visited_cell_directions_by_coord = {}
        active_paths_so_far = [ (s_coord, initial_direction, initial_score) ]  

        found_exit = False
        best_path_score = None
        while active_paths_so_far:
            # print( "active_paths_so_far: ", active_paths_so_far )
            path = active_paths_so_far.pop(0)
            coord, direction, path_score = path
            if coord == e_coord:
                found_exit = True
                best_path_score = path_score
                break


            if coord in visited_cell_directions_by_coord:
                if direction in visited_cell_directions_by_coord[coord]:
                    if path_score >= visited_cell_directions_by_coord[coord][direction]['path_score']:
                        continue

            if not coord in visited_cell_directions_by_coord:
                visited_cell_directions_by_coord[coord] = {
                        direction : {
                            'coord': coord, 
                            'path_score': path_score 
                            },
                    }
            
            cell_directions = visited_cell_directions_by_coord[coord]
            if not direction in cell_directions:
                cell_directions[direction] = {
                    'coord': coord, 
                    'path_score': path_score 
                    }
            else:
                cell_directions[direction]['path_score'] = path_score

            x, y = coord

            for dd in [0,-1,1]:
                new_direction = (direction + dd) % 4
                dx, dy = coord_delta_by_direction[new_direction]
                new_coord = (x + dx, y + dy)
                new_x, new_y = new_coord
                if char_2d_array[new_y][new_x] == '#':
                    continue
                # anything else is ok
                new_path_score = path_score + 1000 * abs(dd) + 1
                active_paths_so_far.append( (new_coord, new_direction, new_path_score) )

            # sort by path_score, ascending
            active_paths_so_far.sort(key=lambda x: x[2])


        assert found_exit, "No path found"
        return best_path_score

    best_path_score = get_best_path_score( char_2d_array, s_coord, e_coord )

    return {
        'best_path_score': best_path_score,
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

# AOC 2024: 2024-12-23: day16/puzzle1/..
# [{'elapsed_time_s': 0.00023737503215670586},
#  {'elapsed_time_s': 0.00019741710275411606},
#  {'best_path_score': 83444, 'elapsed_time_s': 0.07785720890387893}]