import sys
sys.path.append('../')
sys.path.append('../../')

from utils import *

cases = [
    {
        'input': '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9''',
        'num_safe_reports': 2
    },
    {
        'input': "input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )

    num_safe_reports = 0
    for line in lines:
        levels = list(map(int, line.split()))
        steps = []
        for i in range(1, len(levels)):
            step = levels[i] - levels[i-1]
            steps.append(step)

        # if steps contains 0, continue
        if (0 in steps) or (max(steps)>0 and min(steps)<0):
            continue

        if steps[0] > 0 and max(steps) > 3:
            continue

        if min(steps)<-3:
            continue

        num_safe_reports += 1

    return {'num_safe_reports': num_safe_reports }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['num_safe_reports'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-15: day02/puzzle1/..
# [{'num_safe_reports': 606}]