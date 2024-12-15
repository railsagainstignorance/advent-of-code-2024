import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''',
        'sum_muls': 48
    },
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

    do_do = True
    for line in lines:
        matches = re.findall(r'(?:(do)\(\)|(don\'t)\(\)|(mul)\((\d{1,3}),(\d{1,3})\))', line)
        for match in matches:
            cmd = match[0]
            if match[0] == 'do':
                do_do = True
            elif match[1] == "don\'t":
                do_do = False
            
            if match[2] == 'mul' and do_do:
                a = int(match[3])
                b = int(match[4])
                sum_muls += a * b

    return {'sum_muls': sum_muls }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['sum_muls'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-15: day03/puzzle2/..
# [{'sum_muls': 93733733}] That's not the right answer; your answer is too high.
# [{'sum_muls': 84893551}]
