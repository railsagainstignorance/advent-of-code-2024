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
029A
980A
179A
456A
379A''',
    'shortest_sequences_of_button_presses': [
        '029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
        '980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
        '179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
        '456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
        '379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
        ],
    'sum_of_complexities': 126384,
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
    'shortest_sequences_of_button_presses',
    'sum_of_complexities'
    ]

def solve( instance ):
    KEYPAD_VOID_CHAR = '.'

    class Keypad:
        def __init__(self, spec):
            self.output_keypad_str = spec['output_keypad_str']
            self.__parse_output_keypad_str()
            self.initial_finger_char = 'A'
            self.initial_finger_coord = self.output_keypad_by_char[self.initial_finger_char]
            self.__reset()
            self.__check_current_pointing()
        
        def __parse_output_keypad_str( self ):
            char_yx_array = get_char_yx_array_from_input( self.output_keypad_str )
            self.output_keypad_by_coord = {} # [coord] = char
            self.output_keypad_by_char  = {} # [char] = coord
            for y in range( 0, len(char_yx_array) ):
                for x in range(0, len(char_yx_array[0])):
                    char = char_yx_array[y][x]
                    if char == KEYPAD_VOID_CHAR:
                        continue
                    coord = (x,y)
                    self.output_keypad_by_coord[coord] = char
                    self.output_keypad_by_char[char] = coord

        def __reset( self ):
            self.finger_coord = self.initial_finger_coord

        def __check_current_pointing( self ):
            if not self.finger_coord in self.output_keypad_by_coord:
                raise Exception( f"invalid finger_coord={self.finger_coord}" )

        def set_finger_coord( self, coord ):
            self.finger_coord = coord
            self.__check_current_pointing()

        def set_finger_char( self, char ):
            coord = self.output_keypad_by_char[char]
            self.set_finger_coord( coord )

        def get_finger_details( self ):
            coord = self.finger_coord
            char = self.output_keypad_by_coord[ coord ]
            return coord, char

        def calc_key_press_groups_to_generate_target_code( self, target_output_chars: list[str]=[] ):
            key_press_groups = []

            initial_finger_coord = self.initial_finger_coord
            initial_finger_char = self.output_keypad_by_coord[initial_finger_coord]

            # print(f"DEBUG: initial_finger_coord={initial_finger_coord}, initial_finger_char={initial_finger_char}")

            for char in target_output_chars:
                from_finger_details = self.get_finger_details()
                finger_coord, finger_char = from_finger_details
                # print(f"DEBUG: char={char}, finger_coord={finger_coord}, finger_char={finger_char}")
                key_press_group = []
                key_press_groups.append( key_press_group )
                # calc manhattan set of steps from current finger pos to activating output char
                # find all perms
                # filter out any perms which stray over invalid coords

                char_coord = self.output_keypad_by_char[char]
                dist_x = char_coord[0] - finger_coord[0]
                dist_y = char_coord[1] - finger_coord[1]
                delta_coords = [(my_sign(dist_x), 0)] * abs(dist_x) + [(0, my_sign(dist_y))] * abs(dist_y)
                delta_coord_perms = my_distinct_permutations( delta_coords )
                # print(f"DEBUG: char={char}, \ndelta_coords={delta_coords},\ndelta_coord_perms={delta_coord_perms}")

                for dcp in delta_coord_perms:
                    x, y = self.finger_coord
                    # print(f"dcp={dcp}, finger_coord={self.finger_coord}")
                    found_invalid_coord = False
                    for delta_coord in dcp:
                        # print(f"delta_coord={delta_coord}")
                        dx, dy = delta_coord
                        x = x + dx
                        y = y + dy
                        next_coord = (x,y)
                        if not next_coord in self.output_keypad_by_coord:
                            found_invalid_coord = True
                            break
                    if not found_invalid_coord:
                        # print( f"DEBUG: valid dcp={dcp}")
                        delta_chars = [ char_by_coord_delta[dc] for dc in dcp ]
                        delta_chars.append( 'A' )
                        key_press_group.append( delta_chars )

                self.set_finger_char( char )
                to_finger_details = self.get_finger_details()
                # print(f"char={char}, from_finger_details={from_finger_details}, to_finger_details={to_finger_details}, key_press_group={key_press_group}\n")

            return key_press_groups

        def __recursively_expand_key_press_groups_into_full_sequences( 
                self,
                remaining_key_press_groups, 
                sequence_so_far=[],
                full_sequences=[]
                ):

            next_key_press_group = remaining_key_press_groups[0]
            if len(remaining_key_press_groups)==0:
                raise Exception('remaining_key_press_groups should not be empty')
            elif len(remaining_key_press_groups)==1:
                for key_presses in next_key_press_group:
                    full_sequence = sequence_so_far + key_presses
                    full_sequences.append( full_sequence )
            else:
                for key_presses in next_key_press_group:
                    self.__recursively_expand_key_press_groups_into_full_sequences( 
                        remaining_key_press_groups[1:],
                        sequence_so_far + key_presses,
                        full_sequences
                    )
            return full_sequences

        def generate_all_key_press_groups_for_output_codes( self, output_codes ):
            all_generated_key_press_groups_for_output_codes = [] # [ {'output_code': ..., 'key_press_groups': [...] }, ...]

            for output_code in output_codes:
                key_press_groups = self.calc_key_press_groups_to_generate_target_code(output_code)
                full_sequences = self.__recursively_expand_key_press_groups_into_full_sequences( key_press_groups )
                all_generated_key_press_groups_for_output_codes.append( {
                    'output_code': output_code,
                    'key_press_groups': key_press_groups,
                    'full_sequences': full_sequences
                })

            return all_generated_key_press_groups_for_output_codes

        # eof class

    def reverse_keypad_to_generate_input_for_output_codes ( keypad_codes ):
        keycode_str = ''.join(keypad_codes[0])
        if re.search('[0-9]', keycode_str):
           output_keypad_str = '''\
789
456
123
.0A'''
        else:
           output_keypad_str = '''\
.^A
<v>'''
        spec = { 'output_keypad_str': output_keypad_str }
        keypad_experiment = Keypad( spec )
        all_generated_key_press_groups_for_output_codes = keypad_experiment.generate_all_key_press_groups_for_output_codes( keypad_codes )
        return all_generated_key_press_groups_for_output_codes
  
    def keypad_experiment( keypad_codes ):
        all_key_press_groups = reverse_keypad_to_generate_input_for_output_codes( keypad_codes )
        pprint.pp( all_key_press_groups )


    def daisy_chain_keypads( door_keypad_codes ):
        full_sequences_for_output_codes = []

        all_key_press_groups = reverse_keypad_to_generate_input_for_output_codes( door_keypad_codes )
        for group in all_key_press_groups:
            output_code = group['output_code']
            output_code_str = ''.join(output_code)
            full_sequences = group['full_sequences']
            full_sequence_strs = [ ''.join(s) for s in full_sequences ]
            full_sequences_for_output_codes.append( {
                'output_code_str': output_code_str,
                'output_code': output_code,
                'full_sequences': full_sequences,
                'full_sequence_strs1': full_sequence_strs,
            })

        # for output_code_ensemble in full_sequences_for_output_codes:
        #     full_sequence_strs1 = []

        return full_sequences_for_output_codes


    door_keypad_codes = get_char_yx_array_from_input( instance['input'] )

    full_sequences_for_output_codes = daisy_chain_keypads( door_keypad_codes )

    pprint.pp( full_sequences_for_output_codes )

    # keypad_experiment( door_keypad_codes )
    # keypad_experiment( [['^', '<', '^', '<', 'A']] )



    shortest_sequences_of_button_presses = []
    sum_of_complexities = 0

    return {
        'shortest_sequences_of_button_presses': shortest_sequences_of_button_presses,
        'sum_of_complexities': sum_of_complexities
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

