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
        # 'total_price_of_fencing': 140,
        'sides': [ 4, 4, 8, 4, 4 ],
        'total_side_price_of_fencing': 80,
    },
    {
        'input': '''\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE''',
        'areas': [ 17, 4, 4 ],
        # 'total_price_of_fencing': 772,
        'sides': [ 12, 4, 4 ],
        'total_side_price_of_fencing': 236,
    },
    {
        'input': '''\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA''',
        'areas': [ 28, 4, 4 ],
        'sides': [ 12, 4, 4 ],
        'total_side_price_of_fencing': 368,
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
        'areas': [ 12, 4, 14, 10, 13, 11, 1, 13,14, 5, 3 ],
        'sides': [ 10, 4, 22, 12, 10, 12, 4, 8, 16, 6, 6 ],
        # 'total_price_of_fencing': 1930,
        'total_side_price_of_fencing': 1206,
    },
    {
        'input': "../puzzle1/input.txt",
    }
]

attrs = [
    'areas',
    'sides',
    # 'total_price_of_fencing'
    'total_side_price_of_fencing',
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

    def calc_region_sides( region_coords_set ):
        # establish bounding box of region
        # scan bounding box from top left to bottom right
        #  for each region coord, check if it has a nhbr in each cardinal direction, appending coord to list for each direction
        # for each direction, sort the coords
        # for each cardinal direction, count distinct contiguous runs of coords
        # return the sum of the counts

        def get_region_bounding_box( region_coords_set ):
            min_r_x = min([ coord[0] for coord in region_coords_set ])
            max_r_x = max([ coord[0] for coord in region_coords_set ])
            min_r_y = min([ coord[1] for coord in region_coords_set ])
            max_r_y = max([ coord[1] for coord in region_coords_set ])
            return min_r_x, max_r_x, min_r_y, max_r_y
        
        min_r_x, max_r_x, min_r_y, max_r_y = get_region_bounding_box(region_coords_set)

        coords_by_cardinal_direction = { # coords having an outside in the given direction
            0: [], # e
            1: [], # s
            2: [], # w
            3: [], # n
        }

        for y in range(min_r_y, max_r_y+1):
            for x in range(min_r_x, max_r_x+1):
                coord = (x, y)
                if coord not in region_coords_set:
                    continue

                for direction in range(4):
                    dx, dy = coord_delta_by_direction[direction]
                    new_x = x + dx
                    new_y = y + dy

                    new_coord = (new_x, new_y)
                    if new_coord not in region_coords_set: # also encompasses OOBounds
                        coords_by_cardinal_direction[direction].append(coord)
        
        for direction, coords in coords_by_cardinal_direction.items():
            if direction == 0 or direction == 2:
                coords.sort(key=lambda c: c[0])
            else:
                coords.sort(key=lambda c: c[1])

        # print(coords_by_cardinal_direction)
        sides = 0

        for direction, coords in coords_by_cardinal_direction.items():
            if len(coords) == 0:
                continue

            sides += 1
            coord = coords[0]
            for next_coord in coords[1:]:
                combined_abs_delta = abs(next_coord[0] - coord[0]) + abs(next_coord[1] - coord[1])
                if combined_abs_delta > 1:
                    sides += 1
                coord = next_coord
            
        return sides

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
                sides = calc_region_sides(region_coords_set)
                region = { 'char': char, 'coords': region_coords_set, 'area': area, 'perimeter': perimeter, 'sides': sides }
                regions.append( region ) 

        return regions
    
    regions = find_regions()

    areas = [ region['area'] for region in regions ]
    fence_prices = [ region['area'] * region['perimeter'] for region in regions ]
    total_price_of_fencing = sum(fence_prices)

    sides = [ region['sides'] for region in regions ]
    side_prices = [ region['area'] * region['sides'] for region in regions ]
    total_side_price_of_fencing = sum(side_prices)

    return {
        'areas': areas,
        'total_price_of_fencing': total_price_of_fencing,
        'sides': sides,
        'total_side_price_of_fencing': total_side_price_of_fencing,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-21: day12/puzzle2/..
# [{'total_side_price_of_fencing': 901100, 'elapsed_time_s': 0.04278491600416601}]