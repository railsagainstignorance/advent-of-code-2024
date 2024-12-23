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
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<''',
    'final_map': '''\
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########''',
    'sum_of_boxes_GPS_coordinates': 2028,
    },
    {
        'input': '''\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^''',
    'final_map': '''\
##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########''',
    'sum_of_boxes_GPS_coordinates': 10092,
    },
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'final_map',
    'sum_of_boxes_GPS_coordinates',
    ]

def solve( instance ):
    WALL_CHAR  = '#'
    WALL_ID    = -2
    ROBOT_CHAR = '@'
    ROBOT_ID   = -3
    BOX_CHAR   = 'O'
    SPACE_CHAR = '.'
    SPACE_ID   = -1

    def parse_input( input ):
        int_yx_array = []
        boxes = []
        move_directions = []
        robot_coord = None

        strs = get_array_of_strings_from_input( input )
        for y, str in enumerate(strs):
            if str.startswith('#'): # #..O..O.O#
                chars = list(str)
                row = []
                for x, char in enumerate(chars):
                    if char == WALL_CHAR:
                        row.append( WALL_ID )
                    elif char == ROBOT_CHAR: # 
                        row.append( ROBOT_ID )
                        robot_coord = (x,y)
                    elif char == BOX_CHAR:
                        box = {'coord': (x,y), 'id': len(boxes)}
                        boxes.append( box )
                        row.append( box['id'] )
                    elif char == SPACE_CHAR:
                        row.append( SPACE_ID )  
                    else:
                        assert False, f"Unknown char: {char}"
                int_yx_array.append( row )
            elif str == '':
                continue
            else:
                direction_arrows = list(str)
                for da in direction_arrows:
                    direction = direction_by_char_arrow[da]
                    move_directions.append( direction )
        return int_yx_array, boxes, move_directions, robot_coord

    int_yx_array, boxes, move_directions, robot_coord = parse_input( instance['input'] )

    # print( f"int_yx_array: {int_yx_array}" )
    # print( f"boxes: {boxes}" )

    # scan from robot_coord in direction
    # accumulate contiguous line of BOXes along the way
    # until reach a SPACE or a WALL.
    # if SPACE then move the ROBOT and BOXes along one step,
    # if WALL then nothing moves.
    def move_robot_in_direction( direction, int_yx_array, boxes, robot_coord ):
        x, y = robot_coord
        dx, dy = coord_delta_by_direction[direction]
        box_ids_to_move = []
        is_space_to_move_to = False

        while True:
            x,y = x+dx, y+dy
            cell = int_yx_array[y][x] 
            if cell == WALL_ID:
                break
            elif cell >= 0: # is a BOX
                box_ids_to_move.append( cell )
            elif cell == SPACE_ID:
                is_space_to_move_to = True
                break
            else:
                assert False, f"Unknown id: {int_yx_array[y][x]}"

        if is_space_to_move_to:
            # move robot
            x, y = robot_coord
            new_x, new_y = x+dx, y+dy

            robot_coord = (new_x, new_y)
            assert int_yx_array[new_y][new_x] != WALL_ID, f"Robot is moving onto a wall"
            int_yx_array[y][x] = SPACE_ID # only robot leaves a space behind

            # move boxes
            for box_id in box_ids_to_move:
                box = boxes[box_id]
                x, y = box['coord']
                new_x, new_y = x+dx, y+dy
                assert int_yx_array[new_y][new_x] != WALL_ID, f"Box {box_id} is moving onto a wall"
                box['coord'] = (new_x, new_y)
                int_yx_array[new_y][new_x] = box_id

        return int_yx_array, boxes, robot_coord, is_space_to_move_to

    for direction in move_directions:
        int_yx_array, boxes, robot_coord, is_space_to_move_to = move_robot_in_direction( direction, int_yx_array, boxes, robot_coord )

    def construct_map( int_yx_array, robot_coord ):
        row_strs = []
        for y, row in enumerate(int_yx_array):
            char_row = []
            for x, cell in enumerate(row):
                if (x,y) == robot_coord:
                    char_row.append( ROBOT_CHAR )
                elif cell == WALL_ID:
                    char_row.append( WALL_CHAR )
                elif cell == SPACE_ID:
                    char_row.append( SPACE_CHAR )
                else:
                    char_row.append( BOX_CHAR )
            row_strs.append( ''.join(char_row) )    
        
        str = '\n'.join(row_strs)
        return str

    final_map = construct_map( int_yx_array, robot_coord )

    gps_scores= []
    for box in boxes:
        x, y = box['coord']
        gps_scores.append( x + 100*y )

    sum_of_boxes_GPS_coordinates = sum(gps_scores)

    return {
        'sum_of_boxes_GPS_coordinates': sum_of_boxes_GPS_coordinates,
        'final_map': final_map
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

# AOC 2024: 2024-12-23: day15/puzzle1/..
# [{'elapsed_time_s': 4.079192876815796e-05},
#  {'elapsed_time_s': 0.0002447499427944422},
#  {'final_map': '##################################################\n'
#                '#OOOOOO..O..OOOOO#OOO.O..OOO.#.O....O....OO.O....#\n'
#                '#O.........OOOOOOOOOOO...OOO#OOO....O.O#..O..OO..#\n'
#                '#OO.........OO.OOO...........OO...........OO.O...#\n'
#                '#O........#...O.#O........OO..O..........O#..O..##\n'
#                '#O........O..OOO#O.........#...OO....#....#.....##\n'
#                '#...#.......O...O......#..#O...O##....#.O.O..O..O#\n'
#                '#..O.O##O..O....#......#...OO..#OO....O.OOO.OO...#\n'
#                '#.#OOOO...##O....OOO.......O.......OOOOO.#O#...#.#\n'
#                '#.......#..#O..O...........OO....O.#O#....O.OOO..#\n'
#                '#.#..#O.....O.O#.........OO.....O.OOOO.#...OO...##\n'
#                '#O.......OOO#O........O#..OO#.......OO#.#O.#..O..#\n'
#                '#O#.....#OOOO.......O.....OO#OOO....#OO....O#...O#\n'
#                '#.#..#..O##O.....###.....#...O...O..........O#.#.#\n'
#                '##.O....OOO.#...O........O.O##..O.............OOO#\n'
#                '#..O.O..O........OO.........#OOO....O.........OOO#\n'
#                '#O.OOO.#.....O.O......O......OOO..O.O..O......O#.#\n'
#                '#..O#.....O...........................O#OOOO#O...#\n'
#                '###..O...........O....#O.......OO.....#.OO#O.##O.#\n'
#                '#OO.......#.#...#O......OOO.......#...O#OOO#.OO..#\n'
#                '#O.........OOO.O...O#.#.O.#OOO.O...O..O..#O#..O.O#\n'
#                '#OO........OOOOO....OO................##..OO.....#\n'
#                '#.#.#..#.OOOOOO#.##.#OO#..#.OOO..O..........O.##.#\n'
#                '#O..O..##..O#.#O.....#.....O........OO.....OO#...#\n'
#                '#O@..#O.....#.##OO.....O.O...OOO..OOOOO.........O#\n'
#                '#O......#.......##......#O........O#O....O....#.O#\n'
#                '##......OOOO.OO..#..#....OOOO.......O.O#........##\n'
#                '#O..#......#.OOO.....O#..##O.O..#..#..OO.......OO#\n'
#                '#O....O...OO#OO......#O...OOOOOO...O..O......#.O.#\n'
#                '#O........OOOOOOO..........O#O.O....OOO......O.OO#\n'
#                '#..#.#.....OO#.OOOO.........O........OOO.......OO#\n'
#                '#..O.......#....OO.O..#O....#.........OOO......OO#\n'
#                '#.........OOO.....O........#O........O........OOO#\n'
#                '#.......O#.O#......O......O....OO.#..........O#O.#\n'
#                '#OOO...O.....................O#O.#....O#....OOO.O#\n'
#                '#OOO........O#OO....O.....OOO#OOOO...#.#...O.OO.O#\n'
#                '#OO#.#...O..#..#.O#.#O..O#..#OOO#..#O......O.#O..#\n'
#                '#O#.........OO.#.#O.....O#.....OO.O..#.....O..O..#\n'
#                '#OO#..#.....OOOOO..O#..O.#O.#......O..........#.O#\n'
#                '#OO#O............O..OO......................OOO..#\n'
#                '#OO...O#....OOOOOOOO...OO...O.O.O#O....O..#..#O..#\n'
#                '#O..#OOOO..O..O..#O...O#...O#O..OO#..#OOO........#\n'
#                '#...O#O.O.#O..........O#.....O..OOO..O.......#..O#\n'
#                '#.O..OO.O..O.OOOOOOO........O..##O....O.........O#\n'
#                '#.O..#.O....OO....#O....O..#.....OOO#.....#.....O#\n'
#                '#.OO.............#OO.....#........#OO...........O#\n'
#                '#O.O.O.O.......O#OO...............#O......OO..OOO#\n'
#                '#...OO...#O.##OOO.O........#.....O.#OOOOOOO#OOOOO#\n'
#                '#.O..##.OO....##....O#OOOO..O....OOOOOO#O#OO#OOOO#\n'
#                '##################################################',
#   'sum_of_boxes_GPS_coordinates': 1511865,
#   'elapsed_time_s': 0.006890291115269065}]