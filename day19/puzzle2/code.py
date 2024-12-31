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
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb''',
    'num_possible_designs': 6,
    'sum_towel_arrangements': 16,
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'num_possible_designs',
    'sum_towel_arrangements'
    ]

def solve( instance ):

    def parse_input( input ):
        strs = get_array_of_strings_from_input( input )
        towels = list(set(strs.pop(0).split(', ')))
        strs.pop(0)
        designs = strs

        towel_options = '|'.join(towels)
        design_re_str = f"^(?:{towel_options})+$"
        design_prog = re.compile(design_re_str)

        return towels, designs, design_prog

    towels, designs, design_prog = parse_input( instance['input'] )
    # print(f"DEBUG: towels={towels}, designs={designs}")

    def assess_designs( designs, design_prog, towels ):
        num_achievable_designs = 0
        sum_towel_arrangements = 0

        known_counts_by_remaining_design = {} # [remaining_design] = count

        for design in designs:
            m = design_prog.match( design )
            if not m:
                continue

            num_achievable_designs += 1

            # we know this design is achievable
            # find those towels which could contribute to the pattern
            # find all combos of those towels which create the pattern

            possible_towels = [ t for t in towels if t in design ]
            # print( f"DEBUG: design={design}, possible_towels={possible_towels}")

            len_design = len(design)

            # def find_all_towel_combos( combo_csv_strs=set(), towels_so_far=[] ):
            #     towels_so_far_str = ''.join(towels_so_far)
            #     len_towels_so_far_str = len(towels_so_far_str)
            #     print( f"DEBUG: len_towels_so_far_str={len_towels_so_far_str}, len_design={len_design}, len(combo_csv_strs)={len(combo_csv_strs)}")

            #     if not design.startswith( towels_so_far_str ):
            #         return combo_csv_strs

            #     if len_towels_so_far_str > len_design:
            #         return combo_csv_strs
                
            #     if towels_so_far_str == design:
            #         combo_csv_str = ','.join(towels_so_far)
            #         combo_csv_strs.add( combo_csv_str )
            #         return combo_csv_strs

            #     if len_towels_so_far_str == len_design:
            #         return combo_csv_strs

            #     remaining_design = design[len_towels_so_far_str:]

            #     for towel in possible_towels:
            #         if remaining_design.startswith(towel):
            #             if len(towel) + len_towels_so_far_str <= len_design:
            #                 combo_csv_strs = find_all_towel_combos( combo_csv_strs, towels_so_far + [towel] )

            #     return combo_csv_strs

            # combo_csv_strs = find_all_towel_combos()
            # print(f"DEBUG: combo_csv_strs={combo_csv_strs}")

            # sum_towel_arrangements += len( combo_csv_strs )

            def count_towel_combos_matching_remaining_design( remaining_design: str ):
                len_remaining_design = len(remaining_design)
                assert len_remaining_design > 0
                if not remaining_design in known_counts_by_remaining_design:
                    count_matching_remaining = 0
                    for towel in possible_towels:
                        len_towel = len(towel)
                        if len_towel > len_remaining_design:
                            continue
                        if towel == remaining_design:
                            count_matching_remaining += 1
                            continue
                        if len_towel == len_remaining_design:
                            continue
                        if remaining_design.startswith(towel):
                            remaining_remaining_design = remaining_design[len_towel:] 
                            count_matching_remaining += count_towel_combos_matching_remaining_design( remaining_remaining_design )
                            continue 

                    known_counts_by_remaining_design[remaining_design] = count_matching_remaining
            
                return known_counts_by_remaining_design[remaining_design]

            sum_towel_arrangements += count_towel_combos_matching_remaining_design( design )

        return num_achievable_designs, sum_towel_arrangements

    num_possible_designs, sum_towel_arrangements = assess_designs( designs, design_prog, towels )

    return {
        'num_possible_designs': num_possible_designs,
        'sum_towel_arrangements': sum_towel_arrangements,
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

# AOC 2024: 2024-12-31: day19/puzzle2/..
# [{'elapsed_time_s': 9.587500244379044e-05},
#  {'num_possible_designs': 342,
#   'sum_towel_arrangements': 891192814474630,
#   'elapsed_time_s': 0.1358359579462558}]