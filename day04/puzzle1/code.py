import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
..X...
.SAMX.
.A..A.
XMAS.S
.X....''',
        'num_xmas': 4
    },
    {
        'input': '''\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX''',
        'num_xmas': 18
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )
    num_xmas = 0

    max_r = len(lines)
    max_c = len(lines[0])

    for r in range(0, max_r):
        for c in range(0, max_c):
            if lines[r][c] == 'X':
                for d in coord_delta_by_direction_with_diagonals.keys():
                    next_r = r 
                    next_c = c
                    dr, dc = coord_delta_by_direction_with_diagonals[d]

                    gone_wrong = False
                    for letter in 'MAS':
                        next_r = next_r + dr
                        next_c = next_c + dc
                        
                        if next_r < 0 or next_r >= max_r or next_c < 0 or next_c >= max_c:
                            gone_wrong = True
                            break

                        if lines[next_r][next_c] != letter:
                            gone_wrong = True
                            break

                    if not gone_wrong:
                        num_xmas += 1

    return {'num_xmas': num_xmas }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['num_xmas'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-15: day04/puzzle1/..
# [{'num_xmas': 2336}]