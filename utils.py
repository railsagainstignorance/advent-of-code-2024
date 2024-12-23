import os
from datetime import datetime
from timeit import default_timer as timer

ymd = datetime.now().strftime("%Y-%m-%d")

# assorted utils to help refactor the daily aoc code 

def get_string_or_file(input_arg):
    """
    This function takes an input argument, which can be either a string or a filename.
    If it's a filename, it prints the content of the file. If it's just a string, it prints the string itself.
    
    :param input_arg: Either a string or a filename.
    """

    try:
        # Try to open the file if the input_arg is a valid filename
        if len( input_arg )>40:
            raise FileNotFoundError()

        with open(input_arg, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        # If the file is not found, treat the input_arg as a regular string
        return input_arg

def get_array_of_strings_from_input( arg ):
    str = get_string_or_file( arg )
    arr = str.split('\n')
    return arr 

def get_char_yx_array_from_input( arg ):
    # char_2d_array[y][x] = char
    
    row_strs = get_array_of_strings_from_input( arg )
    char_2d_array = [ list(row_str) for row_str in row_strs ]
    return char_2d_array

def get_int_yx_array_from_input( arg ):
    # int_2d_array[y][x] = char
    
    row_strs = get_array_of_strings_from_input( arg )
    int_2d_array = [ list(map(int, list(row_str))) for row_str in row_strs ]
    return int_2d_array

def construct_char_yx_array( width, height, default_char ):
    return [ [default_char for _ in range(width)] for _ in range(height) ]

def construct_int_yx_array( width, height, default_int=0 ):
    return [ [default_int for _ in range(width)] for _ in range(height) ]

def print_here():
    here = __file__ # NB, the path to utils from the code will have a trailing ..
    here_path = os.path.dirname(here)
    folders = here_path.split("/")
    final_folders = folders[-4:-1]
    final_folders_path = "/".join(final_folders)    

    print( "AOC 2024: {}: {}".format(ymd, final_folders_path))

coord_delta_by_direction = { # [up+down direction 0-3] = coord (x,y)
    0: ( 1,  0), # e
    1: ( 0,  1), # s
    2: (-1,  0), # w
    3: ( 0, -1), # n
}

direction_by_char_arrow = {
    '>': 0, # e
    'v': 1, # s
    '<': 2, # w
    '^': 3, # n
}

coord_delta_by_direction_with_diagonals = { # [up+down+diag direction 0-7] = coord (x,y)
    0: ( 1,  0), # e
    1: ( 1,  1), # se
    2: ( 0,  1), # s
    3: (-1,  1), # sw
    4: (-1,  0), # w
    5: (-1, -1), # nw
    6: ( 0, -1), # n
    7: ( 1, -1), # ne
}

coord_delta_by_direction_with_only_diagonals = { # [diag direction 0-3] = coord (x,y)
    0: ( 1,  1), # se
    1: (-1,  1), # sw
    2: (-1, -1), # nw
    3: ( 1, -1), # ne
}

def exercise_fn_with_cases( fn: callable, cases: list[dict], attrs: list[str], verbose=True):
    """
    This function takes a function, a list of cases, and a list of attributes to check.
    It then runs the function with each case.
    If the first specified attr is present, checks if the output matches the expected value for all the attrs.
    verbose=False returnd only the final attr when the case did not specify the first attr (to trim display of final result)
    """

    response = []

    for index, case in enumerate(cases):
        # print( "index={}".format(index) )

        start = timer()
        output = fn( case )
        end = timer()

        response_item = {}
        if attrs[0] in case:
            for v in attrs:
                assert output[v] == case[v], "for case={}, expecting {}={}, but got {}".format(index, v, case[v], output[v] )
            # print( "index={} passed".format(index) )
        elif verbose:
            for v in attrs:
                # print( "index={} {}={}".format(index, v, output[v]) )
                response_item[v] = output[v]
        else:
            final_attr = attrs[-1]
            response_item[final_attr] = output[final_attr]
        
        response_item['elapsed_time_s'] = end - start
    
        if response_item != {}:
            response.append( response_item )
    return response

import unittest # https://docs.python.org/3/library/unittest.html
class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        None

    @classmethod
    def tearDownClass(cls):
        None

    def setUp( self ):
        None

    def tearDown( self ):
        None    
    
    def test_get_char_yx_array_from_input( self ):
        char_2d_array = [ list("abc"), list("def"), list("ghi") ]
        self.assertEqual( char_2d_array[0][0], 'a' )
        self.assertEqual( char_2d_array[1][2], 'f' )

    def test_exercise_fn_with_cases( self ):
        def fn( case ):
            return { 'output': chr(ord(case['input'])+1) }
        attrs = ['output']

        self.assertEqual( exercise_fn_with_cases( fn, [{ 'input': 'a', 'output': 'b' }], attrs ), []                )
        self.assertEqual( exercise_fn_with_cases( fn, [{ 'input': 'a' }],                attrs ), [{'output': 'b'}] )

        # assert exception

        with self.assertRaises(AssertionError):
            exercise_fn_with_cases( fn, [{ 'input': 'a', 'output': 'a' }], attrs )

    def test_construct_char_yx_array( self ):
        char_2d_array = construct_char_yx_array( 2, 3, '.' )
        self.assertEqual( char_2d_array, [['.','.'],['.','.'],['.','.']] )

    def test_construct_int_yx_array( self ):
        int_2d_array = construct_int_yx_array( 2, 3, 0 )
        self.assertEqual( int_2d_array, [[0,0],[0,0],[0,0]] )   

if __name__ == "__main__":
    unittest.main()