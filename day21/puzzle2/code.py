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
    'num_directional_keypads': 2,
    'sum_of_complexities': 126384,
    },    
    {
        'input': "../puzzle1/input.txt",
        'num_directional_keypads': 2,
        'sum_of_complexities': 202274,
    },
    {
        'input': "../puzzle1/input.txt",
        'num_directional_keypads': 25,
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
            self.reset()
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

        def reset( self ):
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

        def get_char_coord( self, char ):
            return self.output_keypad_by_char[char]

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

    def daisy_chain_keypads( door_keypad_codes, num_directional_keypads ):
        all_sequences_for_output_codes = []
        door_keypad_code_strs = []
        for output_code in door_keypad_codes:
            output_code_str = ''.join(output_code)
            sequences_for_output_code = {
                'output_code_str': output_code_str,
                'output_code': output_code,
                'full_sequence_strs': [output_code_str],
            }
            all_sequences_for_output_codes.append( sequences_for_output_code )
            door_keypad_code_strs.append(output_code_str)

        # initial <>^v control pad for 0-9 keypad
        generate_all_full_sequence_strs( all_sequences_for_output_codes, 'full_sequence_strs', 'full_sequence_strs0')

        for i in range(1, num_directional_keypads+1):
            from_name = f"full_sequence_strs{i-1}"
            to_name = f"full_sequence_strs{i}"
            print( f"DEBUG: code_strs={door_keypad_code_strs}, keypads={num_directional_keypads}, i={i}, num seqs={len(all_sequences_for_output_codes[0][from_name])}, min seq length={len(all_sequences_for_output_codes[0][from_name][0])}")
            generate_all_full_sequence_strs( all_sequences_for_output_codes, from_name, to_name )
        
            # only keep the shortest sequences
            for sequences_for_output_code in all_sequences_for_output_codes:
                to_sequences = sequences_for_output_code[to_name]
                min_length = len( to_sequences[0] )
                new_to_sequences = []
                for sequence in to_sequences:
                    if len(sequence) == min_length:
                        new_to_sequences.append( sequence )
                sequences_for_output_code[to_name] = new_to_sequences

        # calc complexities
        sum_of_complexities = 0
        complexities_by_output_code_str = {}

        for sequences_for_output_code in all_sequences_for_output_codes:
            output_code_str = sequences_for_output_code['output_code_str']
            shortest_final_sequence = sequences_for_output_code[to_name][0]
            output_code_int = int(output_code_str.split('A')[0])
            complexity = len(shortest_final_sequence)*output_code_int
            sequences_for_output_code['complexity'] = complexity
            sum_of_complexities += complexity
            complexities_by_output_code_str[output_code_str] = complexity

        return all_sequences_for_output_codes, sum_of_complexities, complexities_by_output_code_str

    memoised_situations = {} # [(level, context, remaining_code_str)] = sequence_length

    memoised_keypads = {} # [level] = keypad

    def keypad_for_level( level: int ): 
        # level==0 => initial directional-numeric keypad, >0 directional-directional
        assert isinstance(level, int)
        assert level>=0 and level<=25

        if not level in memoised_keypads:
            if level <= 1:
                if level==0:
                    output_keypad_str = '''\
789
456
123
.0A'''
                elif level==1:
                    output_keypad_str = '''\
.^A
<v>'''
                
                spec = { 'output_keypad_str': output_keypad_str }
                keypad = Keypad( spec )
            else:
                keypad = memoised_keypads[1] # keypads >0 are all clones of keypad 1

            memoised_keypads[level] = keypad

        return memoised_keypads[level]

    def recursively_find_shortest_sequence_length_for_code( 
            code:list[str]=None, 
            max_level: int=None, 
            level:int=0, 
            context:tuple=None 
            ):
        """
        input params:
        * code = list of chars in the code, e.g. ['9', A']
        * max_level = highest level of keypad
        * level = which keypad is being considered, 0 => initial keypad, 1 => next keypad, ... max_level
        * context = where is the finger currently pointing at this level, e.g. (2,2)
        """

        # print(f"DEBUG: code={code}, max_level={max_level}, level={level}, context={context}")

        assert code      != None
        assert max_level != None
        assert max_level >= 2
        assert len(code) != 0

        code_str = ''.join(code)
        situation = (level, context, code_str)
        if not situation in memoised_situations:
            # stuff happens
            # - get level's keypad
            # - point its finger
            # - generate the sequences for the next code letter
            # - recurse to each variant, obtaining its shortest sequence length
            # - return the shortest sequence length

            keypad = keypad_for_level(level)

            if context == None:
                keypad.reset()
            else:
                keypad.set_finger_coord( context )
        
            key_press_groups = keypad.calc_key_press_groups_to_generate_target_code( code )
            # print( f"DEBUG: key_press_groups={key_press_groups}")

            assert len(key_press_groups)==len(code)

            # key_press_groups: a list of lists of chars
            # DEBUG: key_press_groups=[[['<', 'A']], [['^', 'A']], [['>', '^', '^', 'A'], ['^', '>', '^', 'A'], ['^', '^', '>', 'A']], [['v', 'v', 'v', 'A']]]

            shortest_length_from_each_key_press_group = []

            for key_press_group in key_press_groups:
                shortest_length = None
                for chars in key_press_group:
                    next_length = None
                    if level == max_level:
                        next_length = len(chars)
                    else:
                        next_length = recursively_find_shortest_sequence_length_for_code( 
                            chars, 
                            max_level, 
                            level+1, 
                            None 
                            )

                    if shortest_length == None or next_length < shortest_length:
                        shortest_length = next_length
                shortest_length_from_each_key_press_group.append( shortest_length )

            shortest_combined_length = sum( shortest_length_from_each_key_press_group )
            memoised_situations[situation] = shortest_combined_length

        return memoised_situations[situation]

    def find_all_complexities( door_keypad_codes, num_directional_keypads ):
        stats_by_code = {}
        for code in door_keypad_codes:
            code_str = ''.join(code)
            shortest_sequence_length = recursively_find_shortest_sequence_length_for_code( code, num_directional_keypads )
            code_int = int(code_str.split('A')[0])
            complexity = shortest_sequence_length * code_int
            stats_by_code[code_str] = {
                'code': code,
                'code_int': code_int,
                'shortest_sequence_length': shortest_sequence_length,
                'complexity': complexity,
            }

        complexities = [ s['complexity'] for s in list(stats_by_code.values())]
        sum_of_complexities = sum(complexities)
        return sum_of_complexities, stats_by_code

    door_keypad_codes = get_char_yx_array_from_input( instance['input'] )
    num_directional_keypads = int(instance['num_directional_keypads'])

    # full_sequences_for_output_codes, sum_of_complexities, complexities_by_output_code_str = daisy_chain_keypads( door_keypad_codes, num_directional_keypads )

    # pprint.pp( complexities_by_output_code_str )
    
    # keypad_experiment( door_keypad_codes )
    # keypad_experiment( [['^', '<', '^', '<', 'A']] )

    sum_of_complexities, stats_by_code = find_all_complexities( door_keypad_codes, num_directional_keypads )
    # pprint.pp( stats_by_code )
    # print(f"DEBUG: len(memoised_situations)={len(memoised_situations)}")

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

# AOC 2024: 2025-01-06: day21/puzzle2/..
# [{'elapsed_time_s': 0.00044150021858513355},
#  {'elapsed_time_s': 0.0007987080607563257},
#  {'sum_of_complexities': 245881705840972,
#   'elapsed_time_s': 0.0035173750948160887}]