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
######
#...E#
##..##
#S..##
######''',
    'best_path_score': 2005, # 5 + 2*1000
    'num_tiles_in_any_best_path': 8,
    },    
    {
        'input': '''\
#######
#....E#
##..###
#S..###
#######''',
    'best_path_score': 2006, # 6 + 2*1000
    'num_tiles_in_any_best_path': 9,
    },    
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
    'num_tiles_in_any_best_path': 45,
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
    'num_tiles_in_any_best_path': 64,
    },
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'best_path_score',
    'num_tiles_in_any_best_path'
    ]

def solve( instance ):

    def parse_input( input ):
        strs = get_array_of_strings_from_input( input )
        char_yx_array = [ list(row_str) for row_str in strs ]
        s_coord = None
        e_coord = None
        for y, row in enumerate(char_yx_array):
            for x, char in enumerate(row):
                if char == 'S':
                    s_coord = (x, y)
                if char == 'E':
                    e_coord = (x, y)

        return char_yx_array, s_coord, e_coord

    char_yx_array, s_coord, e_coord = parse_input( instance['input'] )

    def get_best_path_score( char_yx_array, s_coord, e_coord ):
        initial_direction = 0
        initial_score = 0
        initial_all_coords = set()
        initial_all_coords.add( s_coord )

        visited_cell_directions_by_coord = {}
        active_paths_so_far = [ (s_coord, initial_direction, initial_score, initial_all_coords) ]  

        found_exit = False
        best_path_score = None
        best_all_coords = None

        while active_paths_so_far:
            path = active_paths_so_far.pop(0)
            coord, direction, path_score, all_coords = path

            if coord == e_coord:
                if not found_exit:
                    found_exit = True
                    best_path_score = path_score
                    best_all_coords = all_coords.copy()
                elif path_score < best_path_score:
                    assert False, "should not find a later better score"
                elif path_score > best_path_score:
                    pass
                else: # path_score == best_path_score
                    best_all_coords = best_all_coords.union( all_coords )
                continue
            elif found_exit:
                continue

            if not coord in visited_cell_directions_by_coord:
                visited_cell_directions_by_coord[coord] = {}

            if not direction in visited_cell_directions_by_coord[coord]:
                visited_cell_directions_by_coord[coord][direction] = {
                    'coord': coord, 
                    'path_score': path_score,
                    'all_coords': all_coords.copy(),
                    }
            elif path_score > visited_cell_directions_by_coord[coord][direction]['path_score']:
                continue  # ignore this path
            elif path_score == visited_cell_directions_by_coord[coord][direction]['path_score']:
                prev_all_coords = visited_cell_directions_by_coord[coord][direction]['all_coords']
                visited_cell_directions_by_coord[coord][direction]['all_coords'] = prev_all_coords.union(all_coords)
                continue # add this path's coords to the previous paths' coords
            elif path_score < visited_cell_directions_by_coord[coord][direction]['path_score']:
                visited_cell_directions_by_coord[coord][direction] = {
                    'coord': coord, 
                    'path_score': path_score,
                    'all_coords': all_coords.copy(),
                    }
            
            x, y = coord

            for dd in [0,-1,1]:
                new_direction = (direction + dd + 4) % 4
                dx, dy = coord_delta_by_direction[new_direction]
                new_x, new_y = x + dx, y + dy
                new_coord = (new_x, new_y)
                if char_yx_array[new_y][new_x] == '#':
                    continue
                # anything else is ok
                new_path_score = path_score + 1000 * abs(dd) + 1
                new_all_coords = all_coords.copy()
                new_all_coords.add( new_coord )
                active_paths_so_far.append( (new_coord, new_direction, new_path_score, new_all_coords) )

            # sort by path_score, ascending
            active_paths_so_far.sort(key=lambda x: x[2])

        assert found_exit, "No path found"
        return best_path_score, best_all_coords

    best_path_score, best_all_coords = get_best_path_score( char_yx_array, s_coord, e_coord )

    num_tiles_in_any_best_path = len(best_all_coords)

    return {
        'best_path_score': best_path_score,
        'num_tiles_in_any_best_path': num_tiles_in_any_best_path,
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

