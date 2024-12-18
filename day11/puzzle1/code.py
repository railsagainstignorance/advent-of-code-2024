import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
125 17''',
        'stones_per_intermediate_blink': [
            [253000, 1, 7],
            [253, 0, 2024, 14168],
            [512072, 1, 20, 24, 28676032],
            [512, 72, 2024, 2, 0, 2, 4, 2867, 6032],
            [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32],
            [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2] 
        ],
        'num_blinks': 25,
        'num_stones': 55312,
    },
    {
        'input': "../puzzle1/input.txt",
        'num_blinks': 25,
    }
]

attrs = [
    'stones_per_intermediate_blink',
    'num_stones'
    ]

def solve( case ):
    input_str = get_string_or_file( case['input'] )
    initial_stones = list(map(int, input_str.split()))

    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    # No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

    def blink_stones( stones ):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            else:
                stone_str = str(stone)
                if len(stone_str) % 2 == 0:
                    half = len(stone_str) // 2
                    new_stones.append(int(stone_str[:half]))
                    new_stones.append(int(stone_str[half:]))
                else:
                    new_stones.append(stone * 2024)
        return new_stones

    stones_per_intermediate_blink = []
    stones = initial_stones

    for blink in range(0, case['num_blinks']):
        next_stones = blink_stones(stones)
        if 'stones_per_intermediate_blink' in case:
            if blink < len(case['stones_per_intermediate_blink']):
                stones_per_intermediate_blink.append(next_stones)
        stones = next_stones

    num_stones = len(stones)

    return {
        'stones_per_intermediate_blink': stones_per_intermediate_blink,
        'num_stones': num_stones,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-18: day11/puzzle1/..
# [{'num_stones': 207683, 'elapsed_time_s': 0.09054466616362333}]