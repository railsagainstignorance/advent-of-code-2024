import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

instances = [
    {
        'input': '''\
125 17''',
        'num_stones_per_intermediate_blink': [3, 4, 5, 9, 13, 22],
        'num_blinks': 25,
        'num_stones': 55312,
    },
    {
        'input': "../puzzle1/input.txt",
        'num_blinks': 25,
    },
    {
        'input': "../puzzle1/input.txt",
        'num_blinks': 75,
    }
]

attrs = [
    'num_stones_per_intermediate_blink',
    'num_stones'
    ]

def solve( instance ):
    input_str = get_string_or_file( instance['input'] )
    initial_stones = list(map(int, input_str.split()))

    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    # No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

    def blink_stones_by_enraving( stones_by_engraving ):
        new_stones_by_engraving = {} # { engraving: count}
        for stone, count in stones_by_engraving.items():
            if stone == 0:
                new_stones_by_engraving[1] = new_stones_by_engraving.get(1, 0) + count
            else:
                stone_str = str(stone)
                if len(stone_str) % 2 == 0:
                    half = len(stone_str) // 2
                    new_stones_by_engraving[int(stone_str[:half])] = new_stones_by_engraving.get(int(stone_str[:half]), 0) + count
                    new_stones_by_engraving[int(stone_str[half:])] = new_stones_by_engraving.get(int(stone_str[half:]), 0) + count
                else:
                    new_stones_by_engraving[stone * 2024] = new_stones_by_engraving.get(stone * 2024, 0) + count
        return new_stones_by_engraving

    initial_stones_by_engraving = { stone: 1 for stone in initial_stones }  
    stones_by_engraving = initial_stones_by_engraving
    num_stones_per_intermediate_blink = []

    for blink in range(1, instance['num_blinks']+1):
        next_stones_by_engraving = blink_stones_by_enraving( stones_by_engraving )
        if 'num_stones_per_intermediate_blink' in instance:
            if blink <= len(instance['num_stones_per_intermediate_blink']):
                total = sum( count for stone, count in next_stones_by_engraving.items() )
                num_stones_per_intermediate_blink.append(total)
        stones_by_engraving = next_stones_by_engraving

    num_stones = sum( count for stone, count in stones_by_engraving.items() )   

    return {
        'num_stones_per_intermediate_blink': num_stones_per_intermediate_blink,
        'num_stones': num_stones,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-19: day11/puzzle2/..
# [{'num_stones': 207683, 'elapsed_time_s': 0.0021543330512940884}, {'num_stones': 244782991106220, 'elapsed_time_s': 0.07047362509183586}]