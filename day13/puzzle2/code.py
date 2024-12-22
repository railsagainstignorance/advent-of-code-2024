import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
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
        'input': '''\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279''',
        'sum_fewest_tokens': 480,
    },
    {
        'input': "../puzzle1/input.txt",
    },
    {
        'input': "../puzzle1/input.txt",
        'add_10000000000000_to_prize_coords': True    
    }
]

attrs = [
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
                'xy_by_label': {}, # 'A': { 'x': 0, 'y': 0}, 'B': {'x':0, 'y':0}, 'P': {'x':0, 'y':0}
                }

        if str.startswith('Button'): # Button A: X+94, Y+34
            m = re.match( r'Button ([A-Z]): X\+(\d+), Y\+(\d+)', str )
            assert m is not None
            label, x, y = m.group(1), int(m.group(2)), int(m.group(3))
            machine['xy_by_label'][label] = { 'x': x, 'y': y }
        
        elif str.startswith('Prize'): # Prize: X=8400, Y=5400
            m = re.match( r'Prize: X=(\d+), Y=(\d+)', str )
            assert m is not None
            x, y = int(m.group(1)), int(m.group(2))
            if 'add_10000000000000_to_prize_coords' in instance and instance['add_10000000000000_to_prize_coords']:
                x += 10000000000000
                y += 10000000000000
            machine['xy_by_label']['P'] = { 'x': x, 'y': y }
            machines.append( machine)
            machine = None

    # print( machines )

    def solve_for_A_and_B( machine ):
        xy_by_label = machine['xy_by_label']
        xA, yA = xy_by_label['A']['x'], xy_by_label['A']['y']
        xB, yB = xy_by_label['B']['x'], xy_by_label['B']['y']
        xP, yP = xy_by_label['P']['x'], xy_by_label['P']['y']

        assert min(xA, xB, xP, yA, yB, yP) > 0
        assert xA*yB != yA*xB
        
        b = (xA*yP - yA*xP) / (xA*yB - yA*xB)
        a = (xP - b*xB) / xA

        if a<0 or b<0 or math.floor(a) != a or math.floor(b) != b:
            return None, None
        
        return int(a), int(b)
    
    fewest_tokens = []
    for machine in machines:
        a, b = solve_for_A_and_B( machine )
        if a != None:
            fewest_tokens.append( 3*a + b )
        else:
            fewest_tokens.append( 0 )

    sum_fewest_tokens = sum( fewest_tokens )

    return {
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

# AOC 2024: 2024-12-22: day13/puzzle2/..
# [{'sum_fewest_tokens': 875318608908, 'elapsed_time_s': 2.3625092580914497e-05}, {'sum_fewest_tokens': 31761, 'elapsed_time_s': 0.001408749958500266}, {'sum_fewest_tokens': 90798500745591, 'elapsed_time_s': 0.0016488751862198114}]