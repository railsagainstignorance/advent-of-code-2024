import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
M.S
.A.
M.S''',
        'num_x_mas': 1
    },
    {
        'input': '''\
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........''',
        'num_x_mas': 9
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )
    num_x_mas = 0

    max_r = len(lines)
    max_c = len(lines[0])

    a_coord_str_counts = {} # coord_str -> count

    for r in range(0, max_r):
        for c in range(0, max_c):
            if lines[r][c] == 'M':
                for delta in coord_delta_by_direction_with_only_diagonals.values():
                    next_r = r 
                    next_c = c
                    dr, dc = delta

                    gone_wrong = False
                    a_coord_str = None

                    for letter in 'AS':
                        next_r = next_r + dr
                        next_c = next_c + dc
                        
                        if next_r < 0 or next_r >= max_r or next_c < 0 or next_c >= max_c:
                            gone_wrong = True
                            break

                        if lines[next_r][next_c] != letter:
                            gone_wrong = True
                            break

                        if letter == 'A':
                            a_coord_str = f"{next_c},{next_r}"

                    if not gone_wrong:
                        if not a_coord_str in a_coord_str_counts:
                            a_coord_str_counts[a_coord_str] = 0

                        a_coord_str_counts[a_coord_str] += 1

    # look for all 'A's which appear twice in a valid diagonal MAS

    num_x_mas = len([count for count in a_coord_str_counts.values() if count == 2])

    return {'num_x_mas': num_x_mas }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['num_x_mas'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-15: day04/puzzle2/..
# [{'num_x_mas': 1831}]