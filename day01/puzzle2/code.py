import sys
sys.path.append('../')
sys.path.append('../../')

from utils import *

cases = [
    {
        'input': '''\
3   4
4   3
2   5
1   3
3   9
3   3''',
        'similarity_score': 31
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

def solve( case ):
    lines = get_array_of_strings_from_input( case['input'] )

    # split lines into col1 and col2
    col1 = []
    col2 = []
    for line in lines:
        cols = line.split()
        col1.append( int(cols[0]) )
        col2.append( int(cols[1]) )
    
    col2_counts = {}
    for c in col2:
        if c not in col2_counts:
            col2_counts[c] = 0
        col2_counts[c] += 1

    # iterate through col1, looking for the same value in col2.
    # if exists, add the value times the col2_count to similarity_score

    similarity_score = 0
    for value in col1:
        if value in col2_counts:
            similarity_score += value * col2_counts[value]

    return { 'similarity_score': similarity_score }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['similarity_score'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-15: day01/puzzle2/..
# [{'similarity_score': 24643097}]