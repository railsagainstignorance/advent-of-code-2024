import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
7|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47''',
        'num_page_ordering_rules': 21,
        'num_updates': 6,
        'num_correctly_ordered_updates': 3,
        'sum_middle_page_numbers': 143,
        'num_incorrectly_ordered_updates': 3,
        'corrected_updates': [
            ['97','75','47','61','53'],
            ['61','29','13'],
            ['97','75','47','29','13']
        ],
        'sum_middle_page_numbers_of_corrected_updates': 123
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )
    sum_middle_page_numbers = 0

    page_ordering_rules = []
    pages_csv_to_produce_in_each_update = []

    for line in lines:
        if '|' in line:
            page_ordering_rules.append( line )
        elif line == '':
            pass
        else:
            pages_csv_to_produce_in_each_update.append( line )

    page0s_by_page1s = {} # page1 -> [page0, ...]
    for rule in page_ordering_rules:
        page0, page1 = rule.split('|')
        if not page1 in page0s_by_page1s:
            page0s_by_page1s[page1] = []
        page0s_by_page1s[page1].append( page0 )

    valid_updates = []
    invalid_updates = []

    for update in pages_csv_to_produce_in_each_update:
        is_valid_update = True
        pages = update.split(',')
        for p0 in range( 0, len(pages) - 1 ):
            page0 = pages[p0]
            for p1 in range( p0 + 1, len(pages) ):
                page1 = pages[p1]
                if page0 in page0s_by_page1s and page1 in page0s_by_page1s[page0]:
                    is_valid_update = False
                    break
            if not is_valid_update:
                break
        if is_valid_update:
            valid_updates.append( pages )
        else:
            invalid_updates.append( pages )

    def sum_middle_page_numbers_of_updates( updates ):
        total = 0
        for update in updates:
            pages = update
            middle_index = int( len(pages)/2 )
            middle_page_num = int( pages[middle_index] )
            total += middle_page_num

        return total

    sum_middle_page_numbers = sum_middle_page_numbers_of_updates( valid_updates )

    corrected_updates = []
    for update in invalid_updates:
        # pages = clone of update
        pages = update.copy()
        num_pages = len(pages)
        new_update = [ pages.pop(0) ]
        # for each remaining page
        # loop over new_update, starting at pos 0, checking page0s_by_page1s
        # if the new page must be to the left the page in the new_update, insert the new page to the left.

        for page in pages:
            page_inserted = False
            for i in range( len(new_update) ):
                page1 = new_update[i]
                if page1 in page0s_by_page1s and page in page0s_by_page1s[page1]:
                    new_update.insert( i, page )
                    page_inserted = True
                    break
            if not page_inserted:
                new_update.append( page )
        
        assert( len(new_update) == num_pages )
        corrected_updates.append( new_update )
    
    sum_middle_page_numbers_of_corrected_updates = sum_middle_page_numbers_of_updates( corrected_updates )


    return {
        'num_page_ordering_rules': len(page_ordering_rules),
        'num_updates': len(pages_csv_to_produce_in_each_update),
        'num_correctly_ordered_updates': len(valid_updates),
        'sum_middle_page_numbers': sum_middle_page_numbers,
        'num_incorrectly_ordered_updates': len(invalid_updates),
        'corrected_updates': corrected_updates,
        'sum_middle_page_numbers_of_corrected_updates': sum_middle_page_numbers_of_corrected_updates
    }

def run():
    print_here()
    attrs = [
        'num_page_ordering_rules', 
        'num_updates', 
        'num_correctly_ordered_updates', 
        'sum_middle_page_numbers', 
        'num_incorrectly_ordered_updates', 
        'corrected_updates', 
        'sum_middle_page_numbers_of_corrected_updates'
        ]
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-16: day05/puzzle2/..
# [{'sum_middle_page_numbers_of_corrected_updates': 4828}]