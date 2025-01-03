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
    'map_of_all_coords': '''\
######
#.OOO#
##OO##
#OOO##
######''',
    'num_tiles_in_any_best_path': 8
    },    
    {
        'input': '''\
#######
#....E#
##..###
#S..###
#######''',
    'best_path_score': 2006, # 6 + 2*1000
    'map_of_all_coords': '''\
#######
#.OOOO#
##OO###
#OOO###
#######''',
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
    'map_of_all_coords': '''\
###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############''',
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
    'map_of_all_coords': '''\
#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################''',
    'num_tiles_in_any_best_path': 64,
    },
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'best_path_score',
    'map_of_all_coords',
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

    def get_best_path_score( char_yx_array, s_coord, e_coord ):
        initial_direction = 0
        initial_score = 0
        from_coord = None
        from_direction = None
        to_coord = s_coord

        visited_cell_directions_by_coord = {}
        active_paths_so_far = [ (from_coord, from_direction, to_coord, initial_direction, initial_score) ]  

        found_exit = False
        best_path_score = None

        while active_paths_so_far:
            path = active_paths_so_far.pop(0)
            from_coord, from_direction, to_coord, to_direction, path_score = path

            # if to_coord == (3,10):
            #     print( f"from_coord: {from_coord}, from_direction: {from_direction}, to_coord: {to_coord}, to_direction: {to_direction}, path_score: {path_score}" )

            if not to_coord in visited_cell_directions_by_coord:
                visited_cell_directions_by_coord[to_coord] = {}

            if not to_direction in visited_cell_directions_by_coord[to_coord]:
                if from_coord != None:
                    assert from_coord in visited_cell_directions_by_coord

                all_coords = {to_coord}
                from_coords = set()
                if from_coord != None:
                    from_all_coords = visited_cell_directions_by_coord[from_coord][from_direction]['all_coords']
                    all_coords = all_coords.union( from_all_coords )
                    from_coords.add( from_coord )
                
                visited_cell_directions_by_coord[to_coord][to_direction] = {
                    'coord': to_coord, 
                    'from_coords': from_coords,
                    'path_score': path_score,
                    'all_coords': all_coords,
                    }
            else:
                to_direction_obj = visited_cell_directions_by_coord[to_coord][to_direction]

                if path_score > to_direction_obj['path_score']:
                    continue # ignore this path
                elif path_score == to_direction_obj['path_score']:
                    if from_coord != None:
                        from_all_coords = visited_cell_directions_by_coord[from_coord][from_direction]['all_coords']
                        new_all_coords = to_direction_obj['all_coords'].union( from_all_coords )
                        new_all_coords.add( from_coord )

                        to_direction_obj['all_coords'] = new_all_coords
                        to_direction_obj['from_coords'].add( from_coord )
                    else:
                        pass

                    continue 
                elif path_score < to_direction_obj['path_score']:
                    all_coords = {to_coord}
                    from_coords = set()
                    if from_coord != None:
                        from_all_coords = visited_cell_directions_by_coord[from_coord][from_direction]['all_coords']
                        all_coords = all_coords.union( from_all_coords )
                        from_coords.add( from_coord )

                    to_direction_obj['from_coords'] = from_coords
                    to_direction_obj['path_score'] = path_score
                    to_direction_obj['all_coords'] = all_coords

            if to_coord == e_coord:
                if not found_exit:
                    found_exit = True
                    best_path_score = path_score
                elif path_score < best_path_score:
                    best_path_score = path_score
                elif path_score > best_path_score:
                    pass
                else: # path_score == best_path_score
                    pass
                continue
            elif found_exit and path_score >= best_path_score:
                continue
            
            x, y = to_coord
            for dd in [0,-1,1]:
                new_direction = (to_direction + dd + 4) % 4
                new_from_coord = to_coord
                new_from_direction = to_direction
                if dd == 0: # go straight ahead              
                    dx, dy = coord_delta_by_direction[new_direction]
                    new_x, new_y = x + dx, y + dy
                    new_coord = (new_x, new_y)
                    if char_yx_array[new_y][new_x] == '#':
                        continue
                    # anything else is ok
                    new_path_score = path_score + 1
                else: # turn left or right
                    new_x, new_y = x, y
                    new_coord = (new_x, new_y)
                    new_path_score = path_score + abs(dd)*1000
                
                active_paths_so_far.append( (new_from_coord, new_from_direction, new_coord, new_direction, new_path_score) )

            # sort by path_score, ascending
            active_paths_so_far.sort(key=lambda x: x[4])

        assert found_exit, "No path found"

        best_all_coords = {s_coord, e_coord}
        for direction in visited_cell_directions_by_coord[e_coord]:
            if best_path_score == visited_cell_directions_by_coord[e_coord][direction]['path_score']:
                all_coords = visited_cell_directions_by_coord[e_coord][direction]['all_coords']
                best_all_coords = best_all_coords.union( all_coords )


        # probe_coord = (3,10)
        # if probe_coord in visited_cell_directions_by_coord:
        #     pprint.pp( visited_cell_directions_by_coord[probe_coord] )

        #     for coord in visited_cell_directions_by_coord:
        #         for direction in visited_cell_directions_by_coord[coord]:
        #             if probe_coord in visited_cell_directions_by_coord[coord][direction]['all_coords']:
        #                 print( f"probe_coord in all_coords of {coord}, direction={direction}")

        return best_path_score, best_all_coords

    def construct_map_of_all_coords( char_yx_array, all_coords ):
        # clone char_yx_array
        all_paths_map = [ row.copy() for row in char_yx_array ]
        for coord in all_coords:
            x, y = coord
            all_paths_map[y][x] = 'O'
        # concatenate into str
        map_of_all_coords = "\n".join( [ "".join(row) for row in all_paths_map ] )
        return map_of_all_coords

    char_yx_array, s_coord, e_coord = parse_input( instance['input'] )

    best_path_score, best_all_coords = get_best_path_score( char_yx_array, s_coord, e_coord )

    num_tiles_in_any_best_path = len(best_all_coords)

    map_of_all_coords = construct_map_of_all_coords( char_yx_array, best_all_coords )

    return {
        'best_path_score': best_path_score,
        'num_tiles_in_any_best_path': num_tiles_in_any_best_path,
        'map_of_all_coords': map_of_all_coords,
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

# AOC 2024: 2024-12-24: day16/puzzle2/..
# [{'elapsed_time_s': 0.00011658412404358387},
#  {'elapsed_time_s': 8.79999715834856e-05},
#  {'elapsed_time_s': 0.0018396659288555384},
#  {'elapsed_time_s': 0.0028672919142991304},
#  {'best_path_score': 83444,
#   'map_of_all_coords': '#############################################################################################################################################\n'
#                        '#...........#.......#.........#.........#.........#.............#...........#...#.......#.....#.......#.......#.......#.....#.........#....O#\n'
#                        '#.#########.#####.#.#######.#.###.#.###.#.#####.###.#.#########.#.#.#######.#.#.#####.#.###.#.#.#####.#.#.###.#####.#.#.###.#.#######.#.###O#\n'
#                        '#.............#...#.........#...#.#.#.....#...#.#...#.#.......#...#.#.....#...#.......#...#.........#.#.#...#.......#...#...#...#...#.#...#O#\n'
#                        '#########.###.#.###.#######.###.#.#.#.#####.#.#.#.###.#.#########.#.#.###.###########.###.#.#######.#.#####.###########.#.###.#.#.#.#.#.#.#O#\n'
#                        '#.......#.#...#...#.#...#.....#.#.#.#.#...#.#...#...#.#.........#.#.#.....................#.....#...#...................#...#.#.#.#.#.#.#.#O#\n'
#                        '#.#####.#.#.###.#.###.#.#.#.###.###.###.#.#########.#.#.#####.#.#.#.#.#.###.###.#.#.#.#.#.#.###.#.#.#####.#.#.#####.#.#.###.#.#.###.#.#.#.#O#\n'
#                        '#...#.....#.#.#.#.....#.#.#...#...#.....#...........#.#.#...#.#.#.#.#.#...#...#.#.#.#.#...#...#.#.#...#...#.#.#...#...#.#.#.#.#...#...#.#.#O#\n'
#                        '#.#.#######.#.#.###.#.#.###.#.###.#.#####.###########.#.###.#.###.#.#.#.#####.#.#.#.#.#########.#.#####.###.#.###.#####.#.#.#.###.#.###.#.#O#\n'
#                        '#.#...#...#.#...#...#.#.............#...#...#.......#.#.....#...#...#...#.....#.#...#.......#...#...#...#...#.....#............OOOOOOOOOOOOO#\n'
#                        '#.###.#.###.#####.#.#.#.#.#.#.#.#####.#.#####.#####.#.#####.###.#.#####.#.###.#.#####.###.#.#.#####.#.###.###.###.#.###.#.###.#O#####.#####.#\n'
#                        '#...#.#.#...#.....#.....#.#...#.#.....#.......#...#.#...#...#.#...#.............#.........#...#.....#.#...........#.#.....#...#O#.#...#...#.#\n'
#                        '#####.#.#.###.#######.###.#.###.#.#############.###.###.#.###.#.#.#####.#.###.#.#.###.#########.#.#.#.#.#####.#####.#.#########O#.#.###.#.###\n'
#                        '#.....#.#.#...#...........#...#...#...........#.....#...#.....#.#.....#.#...#.#.#.#...#.....#.#.#.....................#..OOOOOOO#.#.#...#...#\n'
#                        '#.#####.#.#.#.###.###.#.###########.#######.###.#####.#######.#.#####.#####.###.###.#.###.#.#.#.#.###.#.#####.#######.###O#######.#.#.#####.#\n'
#                        '#...#...#.#.#...#.#...#.#.........#.#.#...#.#...#.....#.....#.#.#...#.....#...#.....#.....#.#...#...#.#...#.......#...#OOO#OOO#.....#.#...#.#\n'
#                        '#.#.###.#.#.###.#.#.#.#.#.#####.###.#.#.#.#.#.#######.#.#####.#.#.#####.#.###.#######.#####.#.#####.#.#.#.#.#####.#.###O###O#O#######.###.#.#\n'
#                        '#.#.#...#.#.#...#.#.#...#.....#.......#.#...#.....#...#.......#.#.#.............#.#...#...#.#.#.....#.#.#.#.....#.#...#OOOOO#O#...........#.#\n'
#                        '#.#.#.###.#.#.#####.#####.#####.#####.#.###.#####.#.###########.#.#.###########.#.#.#.#.###.#.#.###.#.###.#.###.#.###.#######O#.###########.#\n'
#                        '#.#.#.#...#.#...#...#.....#...#.#...#.#.#.#.#...#...#...........#.#.#.#...#...#.#...#.#.#...#.#...#.#...#.#...#.#...#.#OOOOOOO#.....#.......#\n'
#                        '###.#.#.###.###.#.###.#####.#.###.#.###.#.#.#.#.#####.#.#########.#.#.#.#.#.#.#.#.###.#.#.#######.#.###.#.###.#.###.#.#O#.#########.#.#####.#\n'
#                        '#...#...#...#...#.....#...#.#.....#.....#...#.#.#.....#.#...#.....#...#.#...#.#.#...#.#.....#...#.#...#.#...#.#...#.#.#O#.#.........#.....#.#\n'
#                        '#.#####.###.#.#########.#.#.#############.#####.#.#####.#.#.#####.###.#.#####.#.###.#.#####.#.#.#.###.#.###.#.###.###.#O#.#.#############.#.#\n'
#                        '#.....#.......#.........#.#.#.....#.....#.#...#.......#...#...#...#...#...#...#...#.#.....#...#...#...#...#.#...#.....#O#.#.......#.....#...#\n'
#                        '#####.#####.###.#########.#.#.###.#.#####.#.#.#.#############.#.###.#####.#.#####.#.#####.#######.#.#####.#.###.#######O#########.###.###.#.#\n'
#                        '#.....#.#...............#.#.#.#...#...#...#...#.#.........#...#.......#...#.#.#...#.#...#.#.......#.#...#...#.#...#....OOO....#.#.....#...#.#\n'
#                        '#.#####.#.#.###.#.#####.#.#.#.#.###.#.#.###.#.###.#######.#.#########.#.###.#.#.###.#.#.#.#.#####.#.#.#.#####.###.#.#####O###.#.#####.#.#####\n'
#                        '#...#.....#...#.#.#...#.#.#.#.#.#...#.#.#...#...#.....#.#...#.......#.#.#...#.#...#.#.#...#.....#.#.#.#.......#.......#OOO#.........#.#.....#\n'
#                        '###.#####.#.#.#.#.#.###.#.#.#.#.#####.#.#.#.###.###.#.#.###.#.#####.###.#.###.###.#.#.#########.#.###.#######.#.#######O#############.#####.#\n'
#                        '#...#...#...#.#.#.#...#.#...#.#.#.....#.#.....#...#.#.#.....#.#...#.#...#.......#.#.#.........#.#.#...#.....#.........#OOOOO#...............#\n'
#                        '#.###.#.###.#.#.#.#.#.#.#.###.#.#.#####.#.###.###.#.#.###.###.#.###.#.#####.#.###.###.#.###.###.#.#.#######.#.#######.#.###O#.###########.#.#\n'
#                        '#.#...#.#...#.#.#.#...#...#...#.#.#...#.#...#.#.#.#.#...#.#.#.#...#.#.....#.#.#.......#...#.#...#...#.....#.#.....#...#...#O#.#.....#.....#.#\n'
#                        '#.#.###.#.#.#.#.#.#.#######.###.#.#.#.#.#####.#.#.#####.#.#.#.###.#.###.#.#.#.#.#########.#.#.###.#####.#.#.###.###.#####.#O#.#.#.###.#####.#\n'
#                        '#.#.#...#.....#.#...#.......#.#.#...#.#.....#.#...#...#.#...#.....#.#...#.#.#.#.#.........#.#...........#.#...#.....#...#.#O#.#.#.#...#.....#\n'
#                        '#.#.#.###.#.###.###.#.#######.#.#####.#####.#.#.###.#.#.#######.#.#.#.#.#.#.#.#.#.#########.#.###########.###.#######.#.#.#O#.###.#.###.#####\n'
#                        '#.#.#.#.......#.#...#.#.......#.....#.....#...#.#...#...#.......#...#.#...#.#.#.#.........#.......#.....#.............#...#OOOOOOO#...#.....#\n'
#                        '#.#.#.#.###.###.#.###.###.#########.###.#######.###.###.#.#######.#.#.#####.#.#.#####.#####.#.#####.###.###.#.###################O###.#####.#\n'
#                        '#.#.#.#.#.#.....#...#...#.........#...#.........#...#.....#.....#.#.#.....#.#.......#.#.....#.#.....#...#.#.#.....#...#...#.....#O#...#...#.#\n'
#                        '#.#.#.#.#.#.###.#######.#.###.###.###.#.#########.###.#####.###.#.#######.#.#########.#.###.###.#####.#.#.#.#####.#.#.#.#.#.###.#O#.###.#.#.#\n'
#                        '#...#.#...#.#...#.....#.#.#...#.#.#.#.#.....#.....#...#...#.#.#.#.......#.#.......#...#...#.#...#...#.#.....#...#.#.#...#.#.#....O#...#.#...#\n'
#                        '#.###.#.###.#####.###.#.###.###.#.#.#.#####.#.###.#.###.#.#.#.#.###.#####.#######.#.#####.#.#.#####.#.###.#.#.###.#######.#.#####O###.#.#####\n'
#                        '#.#...#.....#.....#.#...#.......#...#.....#.#.#...#.....#...#.............#...#...#.#...#.#...#.....#...#.#.#.....#.......#...#OOO#...#.....#\n'
#                        '###.#####.#.#.#####.#####.###.#.###.#####.#.###.#.#####.#.#######.###.#####.#.#.###.#.###.#.#.#.###.###.###.#####.#.#####.###.#O#O#.#.#####.#\n'
#                        '#...#...............#.....#...#.#.....#...#.....#.#.....#.....#...#...#.#...#.#.......#.....#.#.#.#.#.#.#...#...#...#.....#...#OOO..#...#...#\n'
#                        '#.#####.#####.#.#.#.#.#.#####.###.#####.#######.###.#########.###.#.###.#.#.#.#.#######.###.#.#.#.#.#.#.#.###.#.#######.###.###O#O###.###.###\n'
#                        '#.....#.......#.#.#.#...#...#.#...#.....#.......#...#.......#...#.#.#.....#.#.....#.....#.#.#.#.#.#.....#.....#.......#...#.#..O#O..#...#...#\n'
#                        '#.###.###.#######.#.#.###.#.#.#.###.#############.#########.###.###.#####.#.#######.#####.#.#.#.#.###.#.###.#########.#.###.#.#O#O#.#.#.###.#\n'
#                        '#...#...#.#.....#.#.#.....#.....#...#.......#.....#...........#.....#...#.#...#.....#...#...#.#.#...#.#.....#.......#.#.#...#..O#O#...#...#.#\n'
#                        '#.#####.#.###.#.#.#.#######.#####.###.#####.#.#####.#####.###.#####.#.#.#####.#.###.#.#.#####.#.#.###.#######.#####.#.#.#.###.#O#O###.###.#.#\n'
#                        '#.............#...#...#.....#.....#...#.....#.#.......#.#.....#.#.....#.....#.#.#...#.#...#.....#...#.......#...#.#.#.#.#.#.#.#O#O#.....#.#.#\n'
#                        '###.#####.###########.#.###.#.#####.#.#.#####.#######.#.#####.#.#.#.#######.#.#.#####.###.#.#######.###.#####.#.#.#.#.###.#.#.#O#O#.#.###.#.#\n'
#                        '#...#...#.#...#.....#...#.#.#.....#.#.#.....#.........#.......#...#.#.........#.........#...#...........#...#.#.#.#.#.....#...#OOO..#.....#.#\n'
#                        '#.###.#.###.#.#.###.#####.#.###.#.#.#.#####.#.#.#########.#######.#.#.#######.###########.###.###.#.#####.#.###.#.#.###.###.#.#O#O###.###.#.#\n'
#                        '#.#...#.#...#...#...#.#...#...#.#...#.....#.......#.....#.......#.#.#.........#.....#...#...#.#...#.#...#.#.....#...#...#...#..OOO........#.#\n'
#                        '#.#.###.#.#######.###.#.#.###.#.#.###.#.#######.#.#.###.#######.#.#.#####.#####.###.#.#.#.###.#.###.#.#.#.#########.#####.#.###O#O#.###.#.#.#\n'
#                        '#.#...#...#.......#.#...#.........#.#.#.....#...#...#.#...#...#.#.#...#.#.#...#.#.#...#.#.#...#...#.#.#.#.........#.......#.#..O#O#.#...#.#.#\n'
#                        '#.###.#####.#####.#.#.#########.#.#.#.#####.#.#######.###.#.#.#.#.###.#.#.#.#.#.#.#####.###.#####.#.#.#.#########.#########.#.#O#O#.#.#####.#\n'
#                        '#.#...#...#...#.....#...#.......#.#...#...#...#.....#...#.#.#.#.#...#.#...#.#...............#...#.#...#.#.#.....#.#.......#...#OOO#.#.......#\n'
#                        '#.#.#####.###.#.#.#.###.#.#######.#.###.#.#######.#.#.#.#.###.#.###.#.#.###.#########.#######.#.#.#####.#.#.###.#.#.###.#######O#O#.###.#####\n'
#                        '#.#.........#...#.#...#...#.#.....#...#.#.........#...#.#...#.........#.#...#.......#...#.....#.#.....#...#.#.....#...#.#...#..OOO#...#.#...#\n'
#                        '#.#.#######.###.###.#.#####.#.#######.#.###############.###.#####.#######.#####.###.#.#.#.#####.#####.#####.#.#######.###.#.#.#O#####.#.#.#.#\n'
#                        '#.#.......#...#.....#.........#.#.......#...#.....#.....#.#.....#.#.....#...#...#.....#.#.#...#.#...#.#.....#.......#.#...#...#O....#.#.#.#.#\n'
#                        '#.#.#####.#.#######.#.#.#####.#.#.#######.#.#.#.###.#####.#####.#.#.###.###.#.#######.#.#.###.#.###.#.#.###.#####.#.#.#.#######O###.#.#.#.#.#\n'
#                        '#.#.....#...#.......#.#.#.....#.#.#.#.....#...#.....#.........#.#.#...#.#...#.....#...#...#...#.....#.#...#.#.....#.#...#.....#O..#...#.#.#.#\n'
#                        '#.#.###.#####.#######.###.#####.#.#.#.#.#.#.#.#####.###.#.###.#.#.###.#.#.#######.#.#######.###.#####.#.#.###.#####.#.###.#.#.#O#.#####.#.#.#\n'
#                        '#.....#...#.........#.....#...#.....#...#...#...#.....#.#.#...#.#.#...#.#.#.......#...#.........#.....#.#.....#...#.#...#.#....O..........#.#\n'
#                        '###.#####.#.#####.#.#####.#.#.#######.#.###.###.###.#.#.#.#.#.#.###.###.#.#.#########.#.#####.#.#.#####.#########.#.###.#.###.#O#.###.###.###\n'
#                        '#...#.............#.#...#...#.....#...#.#.#...#.....#...#...#.#...#.#.#.#.....#.....#.......#...#.#...#.#...#...#.#...#.#.#...#O#...#...#...#\n'
#                        '#.#.#.#.###########.#.#.#########.#.#.#.#.###.#########.#.#.#.###.#.#.#.#.###.#.###.#####.#######.#.#.#.#.#.#.#.#.###.#.#.#.###O###.###.###.#\n'
#                        '#.#.#...#.#.......#...#...#...#...#.#.#.#...#...#.........#.....#.#...#.....#.....#.#...#.#.......#.....#.#...#...#...#.#......O..#.....#...#\n'
#                        '#.#.###.#.#.#####.#######.#.###.###.#.#.###.###.#########.#######.###.#####.#######.#.#.###.#######.#####.#######.#.###.###.###O#####.###.#.#\n'
#                        '#.....#...#...#...........#...#...#.#...#.....#.#.....#...#...#...#...#...#...#.....#.#.....#...#...#.#.....#.....#.#.#...#.#..OOOOO#...#.#.#\n'
#                        '###.#.#.#.###.#############.#.###.#.#####.###.#.#.###.###.#.#.#.###.#####.###.#.###.#.#########.#.###.#.###.#.#####.#.###.###.#####O###.#.#.#\n'
#                        '#.....#...#.#.......#.....#.#...#...#.....#...#...#...#...#.#.#.#...#.#...#.....#...#.....#.....#.#.#...#.#.#...#.#.#...#.....#...#O#.#...#.#\n'
#                        '#.#.#.#.###.#######.#.###.#.###.#####.#####.#######.###.#.#.#.#.#.###.#.#############.###.#.#####.#.#.###.#.###.#.#.#.#########.###O#.#####.#\n'
#                        '#.#...#.....#.......#.#.#...#.#.......#...#.....#...#...#...#...#...#.#.........................#.#...#...#.#...#.#.#.....#OOOOOOOOO#.....#.#\n'
#                        '#.#.#.#.###.#.#######.#.#####.###.#####.###.#.#.#.###.#########.###.#.#####################.###.#.#.#.#.###.#.###.#.#.#.###O#########.#.###.#\n'
#                        '#...#...#...#.....#...#.........#...#.........#.#.#...........#.#...#.....#.......#.......#...#...#.....#...#.....#.#.#...#O#OOO#.#...#.....#\n'
#                        '#.#.#.#.#.#######.#.###.###.###.###.###########.#.###.#.###.#.#.#.###.###.#####.#.#.#####.#.#####.#####.#.###.#####.#####.#O#O#O#.#.#########\n'
#                        '#.............#...#.#.....#...#.#.#.......#.....#.....#.........#...#.#.........#...#...#.#.#...#.........#...#...#.....#..OOO#O#...#.......#\n'
#                        '###.#.#######.#.###.#.#######.#.#.#######.#############.###########.#.#####.#########.#.#.###.#.###########.###.#.###.#.#.#####O#.#.#######.#\n'
#                        '#.#.....#...#.#...#.#...#.....#.......#.#.#...................#...........#.#.....#...#.#.....#...#...#.......#.#...#.#.....#.#OOO#.....#...#\n'
#                        '#.###.#.#.#.#.###.#.#####.###########.#.#.#.#.#.###############.#.###.###.###.###.#.#####.#######.#.#.#.###.###.###.#######.#.###O#####.#.#.#\n'
#                        '#.....#.#.#.....#.#.......#.............#.#...#.#...#.....#.....#...#.........#...#...#.........#...#.#.#...#...#...#.......#...#O....#.#.#.#\n'
#                        '###.#.#.#.#######.#.#.###.#.#.###########.#.#.#.#.#.#.###.#.#####.#.###.#######.###.#.#.#.#####.#####.###.#.#.###.###.#######.###O###.#.#.#.#\n'
#                        '#...#.#.#...#.....#...#...#.#.........#...#.#...#.#.#.#.#...#.#...#.....#.....#...#.#...#.#...#.#...#...#.#.#...#...#............O..#.#...#.#\n'
#                        '#.###.#.###.#.#########.###.#####.#.#.#.#.#.###.###.#.#.#.###.#.###########.#####.#.#####.#.###.#.#.###.#.#.###.###.#.###.#.#####O#.#.#######\n'
#                        '#...#.#.#...#.....#...#.#...#.....#.#.#.#.....#.....#...#...................#...#.#.#...#.#.....#.#...#...#.....#.#.#...#.#.....#O#.#.......#\n'
#                        '#.#.###.#.#.#####.#.#.#.#.###.#####.#.#.#####.#.#######.#####.#######.#######.#.#.#.#.#.#.#######.###.#####.#.###.#.#####.#####.#O#########.#\n'
#                        '#.#...#...#...#.#...#...#...#.#.....#.#...#...#.#.....#.#.......#...#.#...#...#.#.#.#.#.#...#.....#.......#.#...#.....#...#.....#O#.........#\n'
#                        '#.###.#######.#.#######.#.#.#.#.#####.###.#.###.#.###.#.#.#####.#.#.###.#.#.###.#.#.#.#.###.#.#####.#####.#.#.#.#####.#.###.#####O#.#########\n'
#                        '#.#...#...#.......#...#.#.#.#.......#.......#.....#...#...#...#...#...#.#.#...#...#...#.#...#.#...#...#...#.#.#...#.....#.#......O..#.......#\n'
#                        '###.###.#.#.#######.#.#.###.#######.#####.#.#.#####.#######.#.#######.#.#.###.#######.#.#.###.#.#####.#.###.#####.#.###.#.#.#.###O#####.###.#\n'
#                        '#...#...#...#.......#...#...#.....#.......#.#.....#.........#.#...#...#.#.#...#.....#...#.....#.#.....#...#.#.....#.......#.#....O....#.#...#\n'
#                        '#.###.#######.###########.#.#.###.#########.#.#####.#.###.###.#.#.#.###.#.#.#.#.###.#.#########.#.#########.#.#####.#####.#.#.###O###.###.#.#\n'
#                        '#.....#.......#...........#.#...#...........#.#.......#...#...#.#.#...#.#.#.#.#...#.#.#.........#...#.......#.....#.#.......#...#O#.#.....#.#\n'
#                        '#.#####.###.#####.#####.#######.#############.#.#######.#.###.#.#####.#.#.#.#####.#.#.#.#######.###.#.#######.###.#.###.###.#.###O#.#######.#\n'
#                        '#.....#...#.#...#...#.#...#.....#.............#.........#...#...#...#.#.#...#.....#.#.#.#.....#.#.........#...#...#...#.#...#.#..O#.....#...#\n'
#                        '#####.###.###.#.###.#.###.#.#####.#####.#.#.###############.#.###.#.#.#.#####.#####.#.#.#.#####.#.#######.###.#.#####.#.#.###.#.#O#####.#.###\n'
#                        '#...#...#.....#.#.#.#.#...#...........#.#.#.............#...#.#...#...#.....#.....#.#...#.#...#.#...#...#...#.#.#.....#.#.#...#..O#.....#...#\n'
#                        '###.###.#######.#.#.#.#.#####.#######.#.#.#.###########.#.#####.#######.###.#####.#.#####.#.#.#.###.#.#.###.###.###.###.#.#.#####O#.#######.#\n'
#                        '#.....#.....#...#.#.#.#...#...........#.#.#.#.....#...#...#.....#...#.#.#.#.......#...#.#...#.....#...#...#...#...#...#.#.#.#...#O#.#.......#\n'
#                        '#.#######.#.#.###.#.#.###.#.#.###.#######.###.###.###.###.#.#####.#.#.#.#.###.#######.#.#.#############.#.###.#.#.#.#.###.#.#.###O#.#.#######\n'
#                        '#.........#.#.#.......#.#...#...#.......#.#...#...#...#...#.......#.#.........#.....#.#...#...#.........#...#...#.#.#.....#...#..OOO........#\n'
#                        '#.#########.#.#######.#.#######.#######.#.#.###.###.###.###########.#########.#.#.###.#.###.#.#.#####.#.#.#.###.#.#####.###.###.#.#O#######.#\n'
#                        '#.....#.....#.#...#...#.......#.#.....#.#...#...#...#...#.....#...#.....#...#.#.#.#...#.....#...#...#.#.#.#.#.#.#.....#...#.#...#.#O#.......#\n'
#                        '#####.#.###.#.#.#.#.###.#####.#.#.###.#.#.###.###.#.#.###.#.#.###.###.#.#.###.#.###.###.#########.###.###.#.#.#.#####.###.###.###.#O#.#.###.#\n'
#                        '#...#...........#.#.#...#.....#.#.#.#...#...#.#...#...#...#.#.....#.#.........#.#...#...#OOO#.....#.......#...#.#.....#.......#...#OOOOO....#\n'
#                        '#.#.#####.#.#####.#.###.#.#####.#.#.#######.#.#######.#####.#####.#.#.###.#####.#.#.#.#.#O#O#.###.#.#######.###.#.#.#############.#.###O###.#\n'
#                        '#.........#.#...#.#.#...#.#...#...#.......#.#...#...#.........#.....#.#...#.....#.#...#.#O#OOO#.....#.....#.#...#.#.#.....#.......#...#OOO#.#\n'
#                        '#.#####.###.#.###.#.#.###.#.#.#.#####.###.#.###.#.#.#########.#.#.###.#.###.#####.#.#####O###O#.#.#.#.###.###.###.###.###.#####.#####.#.#O###\n'
#                        '#...............#.#...#...#...#.......#...#...#...#...#.......#.#.....#.#...#.....#.#OOOOO..#O#.#.#.#.#.....#...#.....#.#.#...#.......#.#OOO#\n'
#                        '#.#.#.###.###.#.#.#########.#.#########.#####.#######.#######.#.#.#####.#.#.#.#####.#O#######O#.###.#.#.###.###.###.###.#.#.#.#####.#######O#\n'
#                        '#.#.#...#.#...#.#.#.......#.#.........#...#.......#.#.......#.#.#.#...#...#.#.#.....#O#OOOOOOO#.....#.#...#...#...#.....#...#.....#.#.....#O#\n'
#                        '#.#.#####.#.###.#.#.#####.#.#########.###.#.#####.#.#######.#.#.#.#.#.#.#####.#.#####O#O#######.#####.###.#.#####.#####.#########.#.#.###.#O#\n'
#                        '#.#.#...........#...#...#...#.......#.#.#.#.#...#...#...#...#.......#...#...#.#OOOOOOO#O#...#.....#.............#...#...#.........#...#.#.#O#\n'
#                        '#.#.#.#.#.#####.#####.#######.#.#####.#.#.###.#.###.#.#.#.###.#######.#.#.#.#.#O#######O#.#.#######.#########.#####.#####.#############.#.#O#\n'
#                        '#.#...#.#.#.......#...#.......#.#.......#.#...#.#.....#.#.#.#.#...#...#.....#.#O#.....#O..#...#.....#...#...#.....#.#.....#.........#...#.#O#\n'
#                        '#.###.#.#.#.#####.###.#.###.#.###.#####.#.#.###.#########.#.#.###.#.###.###.#.#O#.#####O#####.#.#####.#.#.#.#####.#.#.#####.#.#######.#.#.#O#\n'
#                        '#.....#.#.#...#...#...#...#.#.#...#.........#.......#.....#.#.....#...#.#.#...#OOO#OOOOO....#.#.#...#.#...#...#...#.#.#...............#....O#\n'
#                        '#.###.#.#.#.#.#.#.#.#####.#.###.###.###############.#.#####.###.#####.#.#.#######O#O#######.#.#.#.###.#######.#.#.#.#.#.#####.#########.###O#\n'
#                        '#.....#...#.#...#.#.....#...#...#.....#...........#...#.......#.#.....#.#.......#O#O#OOO#.....#.#.#...#.......#.#.#...#.#...#.#...#.......#O#\n'
#                        '#.###.#########.#.###.#.#.#.#.#.#######.#########.#.#######.###.#.#####.###.#####O#O#O#O#.#####.#.#.#####.#####.###.###.#.#.#.#.###.###.###O#\n'
#                        '#.#.............#...#.#...#...........#.#.#.....#.#.#...#...#...#.......#...#OOOOO#OOO#O#.#...#...#.....#...#.....#.....#.#.#...#...#...#OOO#\n'
#                        '#.###.#.###.#######.#.#####.###.#####.#.#.#.###.#.###.#.#.###.###########.###O#########O###.#.#.#.#####.###.#####.#.#####.#.#####.#######O###\n'
#                        '#...........#.......#.#.....#.#.....#...#.#...#.#.....#.#.....#...#.....#OOOOO#.......#O#...#...#.....#.#.........#.#...#.#.....#.#OOOOOOO#.#\n'
#                        '#.###.#####.###.#.#.###.###.#.#.###.#####.#.###.#.#####.#.#####.#.#.###.#O#########.#.#O#.#########.###.#.#######.#.###.#.#####.#.#O#######.#\n'
#                        '#.#...#.....#...#.#.....#...#.#.#.......#...#...#.....#.#.....#.#...#...#O#.......#.#.#OOOOOOOOO#...#...#.#.....#.#.....#...#.....#O#.......#\n'
#                        '#.#.#.#.#####.###.#######.###.#.#.###.###.###.#.#.#####.#####.#.#######.#O#.#.###.#.#.#########O#.#.#.#.###.###.#.#####.###.#.###.#O#.#.#####\n'
#                        '#.#.....#.....#...#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO#.#.#...#.#...#...#..O..#.#.#.....#...#.#...#..OOOOOOOOOOO..#.#...#\n'
#                        '#.###.###.#####.###O#O###.#######.###.#.#.###.###.#.#####.#.#####.#########.#.###.#.###.#.#.###O#.###.#.#####.#####.#.###O###O#.###.#.###.#.#\n'
#                        '#.........#.#.....#O.O#...#.....#.#...#...#...#...#...#...#...#...#.......#.#...#...#...#......O..............#OOOOOOOOOOOOOOO#.....#.....#.#\n'
#                        '###.#######.#.###.#O#O#.###.###.#.#.#.#.###.#.#.#.#.#.#.#####.#.#######.#.###.#.#########.###.#O###.###.#.#####O#.#.#.###.#.#.###########.#.#\n'
#                        '#...#..OOOOOOOOOOOOOOO......#.#.#.#.#.....#.............................#...#.#.......#...#....O....#...#.#OOOOO#...#...#...#...#.......#.#.#\n'
#                        '#.#####O#######.#.###.#######.#.###.#.#.#.#.###.#.###.#####.#.###.#########.#####.###.#.###.###O###.#.#.#.#O###########.#####.#.#.#.###.###.#\n'
#                        '#OOOOOOO....#...#...#.........#.....#...#.#.#...#.....#...#.#.......#.......#...#.#...#.#......OOOOOOOOOOOOO....#.....#...#...#.#.#.#.#.#...#\n'
#                        '#O#O#.#.#.#.#.#####.###.#############.#.#.#.#.#####.###.#.#.#####.#.#.#######.#.###.#.#.#######.#.#####.#.#####.#.###.#.#.#.#.#.#.#.#.#.#.#.#\n'
#                        '#O#O#.#...#...#...#.......................#.#...#...#...#.#.#.......#.........#.....#.#.....#...#.......#...#...#.....#.....#...#.#.#.#.#.#.#\n'
#                        '#O#O#.#########.#.#.#.###.#.###.#####.#.#.#.###.#####.###.#.#.###.###################.#####.#.#.###########.#.#######.#.#####.#####.#.#.#.#.#\n'
#                        '#OOO#...........#.......#.....#...............#.........#...#.............................#...............#...........#.............#.....#.#\n'
#                        '#############################################################################################################################################',
#   'num_tiles_in_any_best_path': 483,
#   'elapsed_time_s': 2.102502375142649}]