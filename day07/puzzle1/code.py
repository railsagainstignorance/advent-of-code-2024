import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20''',
        'num_possibly_true_equations': 3,
        'total_calibration_result': 3749,
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'total_calibration_result'
    ]

def solve( case ):

    lines = get_array_of_strings_from_input(case['input'])
    equations = []
    for line in lines:
        parts = line.split(': ')
        test_value = int(parts[0])
        numbers = list(map(int, parts[1].split(' ')))
        equations.append( {
            'test_value': test_value,
            'numbers': numbers,
        })

    operators = ['+', '*']
    
    def evaluate_equation( equation ):
        numbers = equation['numbers']
        partials = [numbers[0]]
        remaining_numbers = numbers[1:]
        for num in remaining_numbers:
            next_partials = []
            for partial in partials:
                for operator in operators:
                    next_partials.append( eval( f"{partial} {operator} {num}") )
            partials = next_partials
        
        is_possibly_true_equation = (equation['test_value'] in partials)
        return is_possibly_true_equation
    
    num_possibly_true_equations = 0
    total_calibration_result = 0

    for equation in equations:
        is_possibly_true_equation = evaluate_equation( equation )
        if is_possibly_true_equation:
            num_possibly_true_equations += 1
            total_calibration_result += equation['test_value']

    return {
        'num_possibly_true_equations': num_possibly_true_equations,
        'total_calibration_result': total_calibration_result,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-16: day06/puzzle2/..
# [{'num_loops_positions_found': 1434, 'elapsed_time_s': 13.037910167011432}]