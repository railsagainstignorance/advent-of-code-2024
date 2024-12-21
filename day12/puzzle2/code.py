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
        # Find left-most region coord.
        # Start from there, go down and anti-clockwise round region.
        # Given a current coord and direction,
        # - find the next coord ahead in that direction. 
        # -- If it's in the region, chech ahead right.
        # --- If ahead right is in the region, move ahead right, turn right (sides++)
        # --- else ahead (sides no change)
        # -- else turn stay at coord, turn left (sides++)
        # repeat until back at start coord and start direction

        # Find left-most region coord.
        leftmost_coord = None
        for coord in region_coords_set:
            if leftmost_coord is None or coord[0] < leftmost_coord[0]:
                leftmost_coord = coord
        assert leftmost_coord is not None, "No leftmost coord found"

        initial_coord = leftmost_coord
        initial_direction = 1 # down, aka south

        current_coord = initial_coord
        current_direction = initial_direction
        sides = 0

        def turn_anticlockwise( direction ):
            return (direction + 3) % 4
        
        def turn_clockwise( direction ):
            return (direction + 1) % 4
        
        def get_valid_coord_in_direction_or_none( coord, direction ):
            x, y = coord
            dx, dy = coord_delta_by_direction[direction]
            new_x = x + dx
            new_y = y + dy
            if new_x < min_x or new_x > max_x or new_y < min_y or new_y > max_y:
                return None
            return (new_x, new_y)

        while sides==0 or current_coord != initial_coord or current_direction != initial_direction:
            next_coord     = None
            next_direction = None

            coord_ahead = get_valid_coord_in_direction_or_none(current_coord, current_direction)
            if coord_ahead is None:
                next_coord     = current_coord
                next_direction = turn_anticlockwise(current_direction)
                sides += 1
            elif coord_ahead in region_coords_set:
                coord_ahead_right = get_valid_coord_in_direction_or_none(coord_ahead, turn_clockwise(current_direction))
                if coord_ahead_right in region_coords_set:
                    next_coord = coord_ahead_right
                    next_direction = turn_clockwise(current_direction)
                    sides += 1
                else:
                    next_coord = coord_ahead
                    next_direction = current_direction
            else:
                next_coord = current_coord
                next_direction = turn_anticlockwise(current_direction)
                sides += 1

            assert next_coord is not None, "next_coord is None"
            assert next_direction is not None, "next_direction is None"

            current_coord     = next_coord
            current_direction = next_direction

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

