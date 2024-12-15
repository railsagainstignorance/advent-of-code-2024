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
        'num_safe_reports': 4
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )

    def calc_steps_from_levels( levels ):
        steps = []
        for i in range(1, len(levels)):
            step = levels[i] - levels[i-1]
            steps.append(step)
        return steps

    def check_steps_for_safety( steps ):
        if (0 in steps) or (max(steps)>0 and min(steps)<0):
            return False

        if steps[0] > 0 and max(steps) > 3:
            return False

        if min(steps) < -3:
            return False

        return True

    num_safe_reports = 0
    for line in lines:
        levels = list(map(int, line.split()))
        steps = calc_steps_from_levels( levels )

        if check_steps_for_safety( steps ):
            num_safe_reports += 1
            # print( levels, steps, True)
            continue

        # print( levels, steps )

        # remove each element in turn from levels and check again
        for i in range(1, len(levels)+1):

            new_levels = levels[:i-1] + levels[i:]
            new_steps = calc_steps_from_levels( new_levels )
            safe = check_steps_for_safety( new_steps )
            # print( i, new_levels, new_steps, safe )
            if safe:
                num_safe_reports += 1
                break            

    return {'num_safe_reports': num_safe_reports }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['num_safe_reports'] )
    print( response )

if __name__ == "__main__":
    run()

# [{'num_safe_reports': 634}] your answer is too low

# AOC 2024: 2024-12-15: day02/puzzle2/..
# [{'num_safe_reports': 644}]