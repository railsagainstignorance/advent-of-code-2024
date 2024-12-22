import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
from utils import *

instances = [
    {
        'input': '''\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3''',
        'bottom_right': (11-1, 7-1),
        'duration_s': 100,
        'robot_count_per_tile': '''\
......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....''',
        'total_safety_factor': 12,
    },
    {
        'input': "../puzzle1/input.txt",
        'bottom_right': (101-1, 103-1),
        'duration_s': 100,
    },
]

attrs = [
    'robot_count_per_tile',
    'total_safety_factor',
    ]

def solve( instance ):

    strs = get_array_of_strings_from_input( instance['input'] )
    min_x, min_y = 0, 0
    max_x, max_y = instance['bottom_right']

    def parse_strs( strs ):
        robots = []
        for str in strs:
            # p=0,4 v=3,-3
            m = re.match(r"p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)", str)
            robot = {
                'id': len(robots),
                'pos': (int(m.group(1)), int(m.group(2))),
                'vel': (int(m.group(3)), int(m.group(4))),
            }
            robots.append( robot )
        return robots

    robots = parse_strs( strs )
    # print( robots )

    for step in range( instance['duration_s'] ):
        for robot in robots:
            x = robot['pos'][0] + robot['vel'][0]
            y = robot['pos'][1] + robot['vel'][1]
            if x<min_x or x>max_x:
                x = (x + max_x + 1) % (max_x + 1)
            if y<min_y or y>max_y:
                y = (y + max_y + 1) % (max_y + 1)
            robot['pos'] = (x, y)
 
    # construct map of robots
    int_yx_array = construct_int_yx_array( max_x+1, max_y+1 )
    for robot in robots:
        x, y = robot['pos']
        int_yx_array[y][x] += 1
 
    # convert to str, with '.' for zero, and digit for count
    robot_count_per_tile = ""
    for row in int_yx_array:
        for count in row:
            if count == 0:
                robot_count_per_tile += "."
            else:
                robot_count_per_tile += str(count)
        robot_count_per_tile += "\n"

    robot_count_per_tile = robot_count_per_tile.strip()
    # print( robot_count_per_tile )
    # print( robots )

    # count robots in each quadrant
    quadrant_counts = [0, 0, 0, 0]
    for robot in robots:
        x, y = robot['pos']
        if x == max_x/2 or y == max_y/2:
            continue
        x_half = 0 if x < max_x/2 else 1
        y_half = 0 if y < max_y/2 else 1
        quadrant = x_half + 2*y_half
        quadrant_counts[quadrant] += 1

    #  total safety factor is product of counts in each quadrant
    total_safety_factor = math.prod( quadrant_counts )


    return {
        'robot_count_per_tile': robot_count_per_tile,
        'total_safety_factor': total_safety_factor,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-22: day14/puzzle1/..
# [{'total_safety_factor': 225810288, 'elapsed_time_s': 0.01096945907920599}]