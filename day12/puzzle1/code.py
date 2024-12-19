import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

instances = [
    {
        'input': '''\
AAAA
BBCD
BBCC
EEEC''',
        'areas': [ 4, 4, 4, 1, 3 ],
        'total_price_of_fencing': 140,
    },
    {
        'input': '''\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO''',
        'areas': [ 21, 1, 1, 1, 1 ],
        'total_price_of_fencing': 772,
    },
    {
        'input': '''\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE''',
        'areas': [12, 4, 14, 10, 13, 11, 1, 13,14, 5, 3],
        'total_price_of_fencing': 1930,
    },
    {
        'input': "../puzzle1/input.txt",
    }
]

attrs = [
    'areas',
    'total_price_of_fencing'
    ]

def solve( instance ):
    char_yx_array = get_char_yx_array_from_input(instance['input']) # char_2d_array[y][x] = char
    min_x = 0
    max_x = len(char_yx_array[0]) - 1
    min_y = 0
    max_y = len(char_yx_array) - 1

    known_coords_set = set()

    def chase_region_coords( char: str, initial_coord: tuple[int, int] ) -> set[tuple[int, int]]:
        assert initial_coord not in known_coords_set, f"coord {initial_coord} already known"
        candidate_coords = [initial_coord]
        region_coords_set = set() 

        while len(candidate_coords) > 0:
            coord = candidate_coords.pop()
            if coord in known_coords_set:
                continue

            known_coords_set.add(coord)
            region_coords_set.add(coord)

            x, y = coord
            for direction in range(4):
                dx, dy = coord_delta_by_direction[direction]
                new_x = x + dx
                new_y = y + dy
                if new_x < min_x or new_x > max_x or new_y < min_y or new_y > max_y:
                    continue

                new_coord = (new_x, new_y)
                if new_coord in known_coords_set:
                    continue

                if char_yx_array[new_y][new_x] == char:
                    candidate_coords.append(new_coord)

        return region_coords_set

    def calc_region_perimeter( region_coords_set ):
        perimeter = 0
        for coord in region_coords_set:
            x, y = coord
            for direction in range(4):
                dx, dy = coord_delta_by_direction[direction]
                new_x = x + dx
                new_y = y + dy
                if new_x < min_x or new_x > max_x or new_y < min_y or new_y > max_y:
                    perimeter += 1
                    continue

                new_coord = (new_x, new_y)
                if new_coord not in region_coords_set:
                    perimeter += 1
        return perimeter

    def find_regions():
        regions = [] # [ { 'char': char, 'coords': set(), 'area': int }, ... ]

        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                coord = (x, y)
                if coord in known_coords_set:
                    continue

                char = char_yx_array[y][x]
                region_coords_set = chase_region_coords(char, coord)
                area = len(region_coords_set)
                perimeter = calc_region_perimeter(region_coords_set)
                regions.append( { 'char': char, 'coords': region_coords_set, 'area': area, 'perimeter': perimeter } ) 

        return regions
    
    regions = find_regions()

    areas = [ region['area'] for region in regions ]

    fence_prices = [ region['area'] * region['perimeter'] for region in regions ]

    total_price_of_fencing = sum(fence_prices)

    return {
        'areas': areas,
        'total_price_of_fencing': total_price_of_fencing,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-19: day12/puzzle1/..
# [{'total_price_of_fencing': 1473276, 'elapsed_time_s': 0.02630300004966557}]