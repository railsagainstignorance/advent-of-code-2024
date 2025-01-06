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
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02''',
        'z_binary_str': '100', 
        'z_decimal': 4,
    }, 
    {   
        'input': '''\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj''',
        'z_binary_str': '0011111101000', 
        'z_decimal': 2024,
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'z_binary_str',
    'z_decimal',
    ]

def solve( instance ):

    def parse_input( input ):
        # x00: 1
        # x01: 1
        # x02: 1
        # y00: 0
        # y01: 1
        # y02: 0

        # x00 AND y00 -> z00
        # x01 XOR y01 -> z01
        # x02 OR y02 -> z02

        initial_values_by_name = {}
        connections_by_output = {}

        strs = get_array_of_strings_from_input( input )
        for str in strs:
            if ':' in str:
                name, value_str = str.split(': ')
                initial_values_by_name[name] = int(value_str)
            elif '->' in str:
                n1, op, n2, arrow, n3 = str.split(' ')
                connections_by_output[n3] = (n1, n2, op)
            else:
                pass

        return initial_values_by_name, connections_by_output

    def pull_output_values( initial_values_by_name, connections_by_output ):
        all_values_by_name = initial_values_by_name.copy()
        z_names = sorted( [name for name in connections_by_output if name.startswith('z')], reverse=True)

        def recurse_through_connections( output_name ):
            assert output_name in connections_by_output or output_name in initial_values_by_name, f"but output_name={output_name}"
            if not output_name in all_values_by_name:
                n1, n2, op = connections_by_output[output_name]
                n1_value = recurse_through_connections(n1)
                n2_value = recurse_through_connections(n2)

                assert n1_value == 0 or n1_value == 1
                assert n2_value == 0 or n2_value == 1

                value = None
                # AND gates output 1 if both inputs are 1; if either input is 0, these gates output 0.
                # OR gates output 1 if one or both inputs is 1; if both inputs are 0, these gates output 0.
                # XOR gates output 1 if the inputs are different; if the inputs are the same, these gates output 0.

                if op == 'AND':
                    value = n1_value & n2_value
                elif op == 'OR':
                    value = n1_value | n2_value
                elif op == 'XOR':
                    value = n1_value ^ n2_value
                else:
                    raise f"unknown op={op}"

                all_values_by_name[output_name] = value

            return all_values_by_name[output_name]

        for z_name in z_names:
            value = recurse_through_connections( z_name )
            all_values_by_name[z_name] = value

        z_binary_str = ''.join( map(lambda name: str(all_values_by_name[name]), z_names) )
        z_decimal = int( z_binary_str, 2 )

        # print( f"DEBUG: all_values_by_name={all_values_by_name}\n z_names={z_names}")

        return z_binary_str, z_decimal

    #--- eof defs

    initial_values_by_name, connections_by_output = parse_input( instance['input'])
    # print(f"DEBUG: initial_values_by_name={initial_values_by_name}, connections_by_output={connections_by_output}")

    z_binary_str, z_decimal = pull_output_values( initial_values_by_name, connections_by_output )

    return {
        'z_binary_str': z_binary_str,
        'z_decimal': z_decimal,
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

# AOC 2024: 2025-01-06: day24/puzzle1/..
# [{'elapsed_time_s': 1.8416903913021088e-05},
#  {'elapsed_time_s': 4.087504930794239e-05},
#  {'z_binary_str': '1100000110000001011000011000110000100011100110',
#   'z_decimal': 53190357879014,
#   'elapsed_time_s': 0.00039445795118808746}]