import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
import pprint

from utils import *

instances = [
    {
        'input': '''\
123''',
    'length_of_sequence': 1,
    'sum_of_secret_numbers': 15887950,
    },    
    {
        'input': '''\
123''',
    'length_of_sequence': 10,
    'sum_of_secret_numbers': 5908254,
    },    
    {
        'input': '''\
1
10
100
2024''',
    'length_of_sequence': 2000,
    'sum_of_secret_numbers': 37327623,
    },    
    {
        'input': "../puzzle1/input.txt",
        'length_of_sequence': 2000,
    },
]

attrs = [
    'sum_of_secret_numbers'
    ]

def solve( instance ):

    initial_secret_numbers = get_array_of_ints_from_input( instance['input'] )
    length_of_sequence = instance['length_of_sequence']

    # Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    # Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
    # Each step of the above process involves mixing and pruning:

    # To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    # To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
    # After this process completes, the buyer is left with the next secret number in the sequence. The buyer can repeat this process as many times as necessary to produce more secret numbers.

    def prune( a:int ):
        c = a % 16777216
        return c

    assert prune(100000000) == 16113920

    def mix( a:int, b:int ):
        # bitwise XOR
        c = b ^ a
        return c

    assert mix(15,42) == 37

    def evolve( a:int ):
        b = prune( mix( a*64,    a ) )
        c = prune( mix( b // 32, b ) )
        d = prune( mix( c*2048,  c ) )
        return d
        
    assert evolve(123) == 15887950

    evolved_secret_numbers = []

    for sn in initial_secret_numbers:
        next_sn = sn
        for i in range(0,length_of_sequence):
            next_sn = evolve(next_sn)
        evolved_secret_numbers.append( next_sn )

    sum_of_secret_numbers = sum( evolved_secret_numbers )
    return {
        'sum_of_secret_numbers': sum_of_secret_numbers
    }

def run():
    print_here()
    verbose = True
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    if verbose:
        pprint.pp( response )
    else:
        print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2025-01-06: day22/puzzle1/..
# [{'elapsed_time_s': 1.5666941180825233e-05},
#  {'elapsed_time_s': 1.3499986380338669e-05},
#  {'elapsed_time_s': 0.002902250038459897},
#  {'sum_of_secret_numbers': 19854248602, 'elapsed_time_s': 1.6694573750719428}]