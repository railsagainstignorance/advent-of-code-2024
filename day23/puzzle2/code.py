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
        'num_triples_with_a_t': 7,
        'password': 'co,de,ka,ta',
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'num_triples',
    'num_triples_with_a_t',
    'password'
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

        connections_by_name = {} # [c1] = set

        for pair in computer_pairs_list:
            c1, c2 = pair
            if not c1 in connections_by_name:
                connections_by_name[c1] = set()

            if not c2 in connections_by_name:
                connections_by_name[c2] = set()

            connections_by_name[c1].add( c2 )
            connections_by_name[c2].add( c1 )

        return computer_pairs_list, connections_by_name

    def find_all_triples( connections_by_name ):
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

        return num_triples, num_triples_with_a_t, triple_str_set

    def find_all_fully_connected_sets( connections_by_name, triple_str_set ):
        all_names = list( connections_by_name.keys() )
        fully_expanded_set_strs = set()
        candidate_set_strs = list( triple_str_set )

        while( len( candidate_set_strs )>0 ):
            candidate_set_str = candidate_set_strs.pop(0)
            added_connection = False
            names = candidate_set_str.split(',')
            for n1 in names:
                maybe_a_connection = True
                for n2 in connections_by_name[n1]:
                    if n1==n2 or n2 in names:
                        continue
                    for other_n1 in names:
                        if other_n1 == n1:
                            continue
                        if not n2 in connections_by_name[other_n1]:
                            maybe_a_connection = False
                            break

                    if maybe_a_connection and not n2 in names:
                        names.append( n2 )
                        new_candidate_set_str = ','.join( names )
                        candidate_set_strs.append( new_candidate_set_str )
                        added_connection = True
                        break
                if added_connection:
                    break
                else:
                    fully_expanded_set_strs.add( candidate_set_str )

        assert len(fully_expanded_set_strs)>0

        largest_set_str = None
        for set_str in fully_expanded_set_strs:
            if largest_set_str == None or len(set_str)>len(largest_set_str):
                largest_set_str = set_str

        assert largest_set_str != None

        names = sorted( largest_set_str.split(',') )
        password = ','.join(names)

        return password


    #--- eof defs

    computer_pairs_list, connections_by_name = parse_input( instance['input'])
    # print(f"DEBUG: computer_pairs={computer_pairs_list}")

    num_triples, num_triples_with_a_t, triple_str_set = find_all_triples( connections_by_name )

    password = find_all_fully_connected_sets( connections_by_name, triple_str_set )

    return {
        'num_triples': num_triples,
        'num_triples_with_a_t': num_triples_with_a_t,
        'password': password,
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

# AOC 2024: 2025-01-06: day23/puzzle2/..
# [{'elapsed_time_s': 0.00010708300396800041},
#  {'num_triples': 11011,
#   'num_triples_with_a_t': 1043,
#   'password': 'ai,bk,dc,dx,fo,gx,hk,kd,os,uz,xn,yk,zs',
#   'elapsed_time_s': 0.5977501668967307}]