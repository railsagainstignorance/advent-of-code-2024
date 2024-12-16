import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........''',
        'num_antennas': 2,
        'num_unique_antinode_locations': 2,
    },
    {
        'input': '''\
..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........''',
        'num_antennas': 3,
        'num_unique_antinode_locations': 4,
    },
    {
        'input': '''\
..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........''',
        'num_antennas': 4,
        'num_unique_antinode_locations': 4,
    },
    {
        'input': '''\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............''',
        'num_antennas': 7,
        'num_unique_antinode_locations': 14,
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'num_antennas',
    'num_unique_antinode_locations'
    ]

def solve( case ):

    char_yx_array = get_char_yx_array_from_input(case['input'])
    max_x = len(char_yx_array[0])
    max_y = len(char_yx_array)
    min_x = 0
    min_y = 0

    def check_coord_in_bounds(coord):
        x, y = coord
        return x >= min_x and x < max_x and y >= min_y and y < max_y
    
    antenna_locations_by_frequency_char = {} # { frequency: [ (x,y), ... ] }
    num_antennas = 0

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            char = char_yx_array[y][x]
            # 0-9 a-z A-Z
            if char.isalnum():
                if not char in antenna_locations_by_frequency_char:
                    antenna_locations_by_frequency_char[char] = []
                antenna_locations_by_frequency_char[char].append( (x,y) )
                num_antennas += 1

    # for each frequency, loop over each pair of antenna locations
    # and calculate the antinode locations, 
    # based on extrapolating the delta between the two antennas out from each antenna.
    # Store the valid antinode locations in a set.

    valid_antinode_locations = set()

    for frequency, antenna_locations in antenna_locations_by_frequency_char.items():
        for i in range(len(antenna_locations)):
            for j in range(i+1, len(antenna_locations)):
                location_i = antenna_locations[i]
                location_j = antenna_locations[j]

                delta_x = location_j[0] - location_i[0]
                delta_y = location_j[1] - location_i[1]

                antinode_i = (location_i[0] - delta_x, location_i[1] - delta_y)
                antinode_j = (location_j[0] + delta_x, location_j[1] + delta_y)

                if check_coord_in_bounds(antinode_i):
                    valid_antinode_locations.add(antinode_i)
                if check_coord_in_bounds(antinode_j):
                    valid_antinode_locations.add(antinode_j)

    num_unique_antinode_locations = len(valid_antinode_locations)

    return {
        'num_antennas': num_antennas,
        'num_unique_antinode_locations': num_unique_antinode_locations,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-16: day08/puzzle1/..
# [{'num_unique_antinode_locations': 359, 'elapsed_time_s': 0.0004539999645203352}]