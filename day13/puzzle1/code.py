import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

instances = [
    {
        'input': '''\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279''',
        'button_pushes': [ (80,40), None, (38, 86), None ],
        'fewest_tokens': [ 280, 0, 200, 0 ],
        'sum_fewest_tokens': 480,
    },
    {
        'input': "../puzzle1/input.txt",
    }
]

attrs = [
    'button_pushes',
    'fewest_tokens',
    'sum_fewest_tokens',
    ]

def solve( instance ):

    strs = get_array_of_strings_from_input( instance['input'] )

    machines = []
    machine = None

    # parse input
    for str in strs:
        if machine == None:
            machine = {
                'button_labels': [],
                'button_deltas': [],
                'prize_coord': (0,0),
                }

        if str.startswith('Button'): # Button A: X+94, Y+34
            m = re.match( r'Button ([A-Z]): X\+(\d+), Y\+(\d+)', str )
            assert m is not None
            machine['button_labels'].append( m.group(1) )
            machine['button_deltas'].append( (int(m.group(2)), int(m.group(3)) ) )
        
        elif str.startswith('Prize'): # Prize: X=8400, Y=5400
            m = re.match( r'Prize: X=(\d+), Y=(\d+)', str )
            assert m is not None
            machine['prize_coord'] = (int(m.group(1)), int(m.group(2)))
            machines.append( machine)
            machine = None

    button_pushes = []
    fewest_tokens = []

    # establish bounds on button presses
    for machine in machines:
        machine['button_min_max_presses'] = []
        for b in range( len(machine['button_deltas']) ):
            max_presses = []
            for i in range( len(machine['prize_coord']) ):
                max_presses.append( int( machine['prize_coord'][i] / machine['button_deltas'][b][i] ) )
            machine['button_min_max_presses'].append( min(max_presses) )

    # brute force all possible button presses
    for machine in machines:
        prize_coord = machine['prize_coord']
        valid_presses_with_tokens = []
        for a_press in range( 0, machine['button_min_max_presses'][0] + 1 ):
            a_delta = machine['button_deltas'][0]
            for b_press in range( 0, machine['button_min_max_presses'][1] + 1 ):
                b_delta = machine['button_deltas'][1]

                coord = (a_press*a_delta[0] + b_press*b_delta[0], a_press*a_delta[1] + b_press*b_delta[1])
                if coord == prize_coord:
                    valid_presses_with_tokens.append( (a_press, b_press, a_press*3 + b_press) )

        best_pushes = None
        best_tokens = 0
        if len(valid_presses_with_tokens) >= 1:
            for valid_pushes in valid_presses_with_tokens:
                if best_pushes == None or valid_pushes[2] < best_tokens:
                    best_pushes = (valid_pushes[0], valid_pushes[1])
                    best_tokens = valid_pushes[2]    

        button_pushes.append( best_pushes ) 
        fewest_tokens.append( best_tokens )

    sum_fewest_tokens = sum( fewest_tokens )

    return {
        'button_pushes': button_pushes,
        'fewest_tokens': fewest_tokens,
        'sum_fewest_tokens': sum_fewest_tokens,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-21: day13/puzzle1/..
# [{'sum_fewest_tokens': 31761, 'elapsed_time_s': 1.0757121669594198}]