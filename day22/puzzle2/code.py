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
        'length_of_sequence': 9,
        'sum_of_secret_numbers': 7753432,
        'most_bananas_sequence_str': '[-1, -1, 0, 2]',
        'most_bananas': 6,
    },    
    {        
        'input': '''\
1
2
3
2024''',
        'length_of_sequence': 2000,
        'sum_of_secret_numbers': 37990510,
        'most_bananas_sequence_str': '[-2, 1, -1, 3]',
        'most_bananas': 23,
    },    
    {
        'input': "../puzzle1/input.txt",
        'length_of_sequence': 2000,
    },
]

attrs = [
    'sum_of_secret_numbers',
    'most_bananas_sequence_str',
    'most_bananas',
    ]

def solve( instance ):

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

    def price_of( num ):
        return int(str(num)[-1])

    def evolve_secret_numbers( initial_secret_numbers: list[int], length_of_sequence ):
        evolved_secret_numbers = []
        prices_by_price_change_quad = {} # ['-1,2,3,-4'] = 6

        for sn in initial_secret_numbers:
            price_change_sequence = []
            next_sn = sn
            price_change_quads_known_to_buyer = set()

            for i in range(0,length_of_sequence):
                prev_sn = next_sn
                next_sn = evolve(next_sn)
                next_price = price_of(next_sn)
                price_change = next_price - price_of(prev_sn)
                price_change_sequence.append( price_change )
                # print(f"DEBUG: next_sn={next_sn}, next_price={next_price}, price_change={price_change}")
                if i>=3:
                    price_change_quad_ints = price_change_sequence[-4:]
                    assert len(price_change_quad_ints)==4, f"but i={i}, price_change_sequence={price_change_sequence}, price_change_quad_ints={price_change_quad_ints}"
                    price_change_quad = f"{price_change_quad_ints}"
                    if price_change_quad in price_change_quads_known_to_buyer:
                        continue
                    else:
                        price_change_quads_known_to_buyer.add( price_change_quad )

                    if not price_change_quad in prices_by_price_change_quad:
                        prices_by_price_change_quad[price_change_quad] = 0
                    prices_by_price_change_quad[price_change_quad] += next_price
                    # if  price_change_quad == '[-2, 1, -1, 3]':
                    #     print(f"DEBUG: price_change_quad={price_change_quad}, next_price={next_price}")

            evolved_secret_numbers.append( next_sn )
            # print( f"DEBUG: price_change_sequence={price_change_sequence}, \nevolved_secret_numbers={evolved_secret_numbers}" )

        return evolved_secret_numbers, prices_by_price_change_quad
    
    def find_most_bananas( prices_by_price_change_quad: dict[int] ):
        most_bananas_sequence_str = None
        most_bananas = None

        for price_change_quad in prices_by_price_change_quad:
            price = prices_by_price_change_quad[price_change_quad]
            if most_bananas_sequence_str == None or price>most_bananas:
                most_bananas_sequence_str = price_change_quad
                most_bananas = price

        return most_bananas_sequence_str, most_bananas

    #--- eof defs

    initial_secret_numbers = get_array_of_ints_from_input( instance['input'] )
    length_of_sequence = instance['length_of_sequence']

    evolved_secret_numbers, prices_by_price_change_quad = evolve_secret_numbers( initial_secret_numbers, length_of_sequence )
    # pprint.pp( prices_by_price_change_quad)
    sum_of_secret_numbers = sum( evolved_secret_numbers )

    most_bananas_sequence_str, most_bananas = find_most_bananas( prices_by_price_change_quad )

    return {
        'sum_of_secret_numbers': sum_of_secret_numbers,
        'most_bananas_sequence_str': most_bananas_sequence_str,
        'most_bananas': most_bananas,
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

# AOC 2024: 2025-01-06: day22/puzzle2/..
# [{'elapsed_time_s': 3.754091449081898e-05},
#  {'elapsed_time_s': 0.011375583009794354},
#  {'sum_of_secret_numbers': 19854248602,
#   'most_bananas_sequence_str': '[1, 0, -1, 1]',
#   'most_bananas': 2223,
#   'elapsed_time_s': 6.7512007500045}]