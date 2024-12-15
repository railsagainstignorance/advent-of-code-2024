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
        'total_distance': 11
    },
    {
        'input': "input.txt"
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
    
    # sort col1 and col2
    col1.sort()
    col2.sort()

    # iterate through col1 and col2, adding the abs difference to total_distance

    total_distance = 0
    for i in range(0, len(col1)):
        total_distance += abs(col1[i] - col2[i])

    return { 'total_distance': total_distance }

def run():
    print_here()
    response = exercise_fn_with_cases( solve, cases, ['total_distance'] )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: day01/puzzle1/..
# [{'total_distance': 2769675}]