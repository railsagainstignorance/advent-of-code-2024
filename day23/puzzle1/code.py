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
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn''',
        'num_triples': 12, 
        'num_triples_with_a_t': 7
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'num_triples',
    'num_triples_with_a_t',
    ]

def solve( instance ):

    def parse_input( input ):
        # kh-tc
        # qp-kh
        # de-cg

        strs = get_array_of_strings_from_input( input )
        computer_pairs_list = []
        for str in strs:
            pair = sorted( str.split('-') )
            computer_pairs_list.append( pair )

        return computer_pairs_list

    def find_all_triples( computer_pairs_list ):
        connections_by_name = {} # [c1] = set

        for pair in computer_pairs_list:
            c1, c2 = pair
            if not c1 in connections_by_name:
                connections_by_name[c1] = set()

            if not c2 in connections_by_name:
                connections_by_name[c2] = set()

            connections_by_name[c1].add( c2 )
            connections_by_name[c2].add( c1 )

        all_names = list( connections_by_name.keys() )
        all_names_starting_with_t = [n for n in all_names if n.startswith('t')]
        triple_str_set = set()

        for n1 in all_names:
            n1_set = connections_by_name[n1]
            for n2 in n1_set:
                if n1==n2:
                    continue
                n2_set = connections_by_name[n2]
                for n3 in n2_set:
                    if n3 in n1_set:
                        if n3 == n1 or n3 == n2:
                            continue
                        triple_str = ','.join( sorted([n1, n2, n3]) )
                        triple_str_set.add( triple_str )

        num_triples = len( triple_str_set )
        triples_with_a_t = [ t for t in triple_str_set if (t.startswith('t') or ',t' in t)]
        num_triples_with_a_t = len(triples_with_a_t)

        return num_triples, num_triples_with_a_t

    #--- eof defs

    computer_pairs_list = parse_input( instance['input'])
    # print(f"DEBUG: computer_pairs={computer_pairs_list}")

    num_triples, num_triples_with_a_t = find_all_triples( computer_pairs_list )

    return {
        'num_triples': num_triples,
        'num_triples_with_a_t': num_triples_with_a_t,
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

# AOC 2024: 2025-01-06: day23/puzzle1/..
# [{'elapsed_time_s': 6.920797750353813e-05},
#  {'num_triples': 11011,
#   'num_triples_with_a_t': 1043,
#   'elapsed_time_s': 0.025911707896739244}]