import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))''',
        'sum_muls': 161
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )
    sum_muls = 0

    for line in lines:
        matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', line)
        for match in matches:
            a = int(match[0])
            b = int(match[1])
            sum_muls += a * b

    return {'sum_muls': sum_muls }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['sum_muls'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-15: day03/puzzle1/..
# [{'sum_muls': 160672468}]