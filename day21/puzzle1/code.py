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
    'sum_of_complexities': 126384,
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
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
                full_sequences=None
                ):

            if full_sequences==None:
                full_sequences = []

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

        def generate_key_press_details_for_output_code( self, output_code ):

            key_press_groups = self.calc_key_press_groups_to_generate_target_code(output_code)
            full_sequences = self.__recursively_expand_key_press_groups_into_full_sequences( key_press_groups )

            key_press_details = {
                'output_code': output_code,
                'key_press_groups': key_press_groups,
                'full_sequences': full_sequences
                }

            return key_press_details

        def generate_all_key_press_details_for_output_codes( self, output_codes ):
            all_generated_key_press_details_for_output_codes = [] # [ {'output_code': ..., 'key_press_groups': [...] }, ...]

            for output_code in output_codes:
                key_press_details = self.generate_key_press_details_for_output_code( output_code )
                all_generated_key_press_details_for_output_codes.append( key_press_details )

            return all_generated_key_press_details_for_output_codes

        # eof class

    def reverse_keypad_to_generate_input_for_output_codes( keypad_codes ):
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
        all_generated_key_press_details_for_output_codes = keypad_experiment.generate_all_key_press_details_for_output_codes( keypad_codes )
        return all_generated_key_press_details_for_output_codes
  
    def reverse_keypad_to_generate_input_for_output_code( keypad_code ):
        all_generated_key_press_details_for_output_codes = reverse_keypad_to_generate_input_for_output_codes( [keypad_code] )
        assert len(all_generated_key_press_details_for_output_codes)==1
        return all_generated_key_press_details_for_output_codes[0]

    def keypad_experiment( keypad_codes ):
        all_key_press_groups = reverse_keypad_to_generate_input_for_output_codes( keypad_codes )
        pprint.pp( all_key_press_groups )

    def generate_all_full_sequence_strs( all_sequences_for_output_codes, from_full_name, to_full_name ):
        for sequences_for_output_code in all_sequences_for_output_codes:
            output_code = sequences_for_output_code['output_code']
            to_full_sequences = []
            for sequence_str in sequences_for_output_code[from_full_name]:
                sequence = list(sequence_str)
                # print(f"output_code={output_code}, sequence_str={sequence_str}")
                key_press_details = reverse_keypad_to_generate_input_for_output_code( sequence )
                to_full_sequences.extend( key_press_details['full_sequences'] )

            to_full_sequence_strs = [ ''.join(s) for s in to_full_sequences ]
            to_full_sequence_strs.sort( key=len )
            sequences_for_output_code[to_full_name] = to_full_sequence_strs

    def daisy_chain_keypads( door_keypad_codes ):
        all_sequences_for_output_codes = []
        for output_code in door_keypad_codes:
            output_code_str = ''.join(output_code)
            sequences_for_output_code = {
                'output_code_str': output_code_str,
                'output_code': output_code,
                'full_sequence_strs': [output_code_str],
            }
            all_sequences_for_output_codes.append( sequences_for_output_code )

        # initial <>^v control pad for 0-9 keypad
        generate_all_full_sequence_strs( all_sequences_for_output_codes, 'full_sequence_strs', 'full_sequence_strs1')

        #  <>^v control pad to <>^v control pad
        generate_all_full_sequence_strs( all_sequences_for_output_codes, 'full_sequence_strs1', 'full_sequence_strs2')

        #  <>^v control pad to <>^v control pad
        generate_all_full_sequence_strs( all_sequences_for_output_codes, 'full_sequence_strs2', 'full_sequence_strs3')

        # calc complexities
        sum_of_complexities = 0
        complexities_by_output_code_str = {}

        for sequences_for_output_code in all_sequences_for_output_codes:
            output_code_str = sequences_for_output_code['output_code_str']
            shortest_final_sequence = sequences_for_output_code['full_sequence_strs3'][0]
            output_code_int = int(output_code_str.split('A')[0])
            complexity = len(shortest_final_sequence)*output_code_int
            sequences_for_output_code['complexity'] = complexity
            sum_of_complexities += complexity
            complexities_by_output_code_str[output_code_str] = complexity

        return all_sequences_for_output_codes, sum_of_complexities, complexities_by_output_code_str

    door_keypad_codes = get_char_yx_array_from_input( instance['input'] )

    full_sequences_for_output_codes, sum_of_complexities, complexities_by_output_code_str = daisy_chain_keypads( door_keypad_codes )

    pprint.pp( complexities_by_output_code_str )

    # keypad_experiment( door_keypad_codes )
    # keypad_experiment( [['^', '<', '^', '<', 'A']] )

    return {
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

# AOC 2024: 2025-01-02: day21/puzzle1/..
# {'029A': 1972, '980A': 58800, '179A': 12172, '456A': 29184, '379A': 24256}
# {'319A': 22330, '670A': 45560, '349A': 25128, '964A': 69408, '586A': 39848}
# [{'elapsed_time_s': 6.914480000035837},
#  {'sum_of_complexities': 202274, 'elapsed_time_s': 99.75852120807394}]