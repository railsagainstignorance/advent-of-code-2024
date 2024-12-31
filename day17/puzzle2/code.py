import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
import pprint

from utils import *

instances = [
#     {
#         'input': '''\
# Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0''',
#     'output_after_halting_csv': '4,6,3,5,6,3,5,2,1,0'
#     },    
    {
        'input': '''\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0''',
    'decorrupt_register_A': True,
    'correct_A': 117440,
    'output_after_halting_csv': '0,3,5,4,3,0',
    },    
    {
        'input': "../puzzle1/input.txt",
        'decorrupt_register_A': True,
    },
]

attrs = [
    'correct_A',
    'output_after_halting_csv'
    ]

def solve( instance ):

    def parse_input_into_spec( input_str ):
        strs = get_array_of_strings_from_input( input_str )
        # Register A: 729
        # Register B: 0
        # Register C: 0

        # Program: 0,1,5,4,3,0
        
        registers = {}
        program_ints = []

        for line in strs:
            m = re.match(r'Register (\w): (\d+)', line)
            if m:
                register = m.group(1)
                value = int(m.group(2))
                registers[register] = value
            
            m = re.match(r'Program: (.+)', line)
            if m:
                program_str = m.group(1)
                program_ints = list(map(int, program_str.split(',')))


        spec = {
            'registers': registers,
            'program_ints': program_ints,
        }

        return spec

    class Computer:
        def __init__(self, spec):
            self.spec = spec
            self.program_ints = spec['program_ints']
            self.program_ints_csv = ','.join(map(str, self.program_ints))
            self.num_program_operands = len(self.program_ints) // 2
            self.reset()

        def reset(self):
            self.pc = 0
            self.output_ints = []
            self.registers = self.spec['registers'].copy()

        def get_output_as_csv(self):
            return ','.join(map(str, self.output_ints))

        def run_until_halting(self, max_steps=10000, max_outputs=16):
            while True:
                if self.pc < 0 or self.pc >= len(self.program_ints):
                    break
                self.run_one_instruction()
            output = self.get_output_as_csv()
            return output
        
        def run_until_halting_or_deviates( self, target_output, max_steps=10000):
            step = 0
            state = None
            while step < max_steps:
                step += 1
                assert self.pc >= 0
                if self.pc >= len(self.program_ints):
                    state = "HALTED"
                    break
                single_output = self.run_one_instruction()
                if single_output is not None:
                    output_so_far = self.get_output_as_csv()
                    # if len(output_so_far) > 1:
                    #     print( f"step={step}: output_so_far={output_so_far}" )
                    if not target_output.startswith(output_so_far):
                        state = "DEVIATED"
                        break

            if step >= max_steps:
                state = "MAXED"

            # if step == 9:
            #     print( f"step={step}: output_so_far={output_so_far}, pc={self.pc}, registers={self.registers}" )

            output = self.get_output_as_csv()
            return output, step, self.output_ints, state
        
        def get_combo_operand(self, operand):
            # Combo operands 0 through 3 represent literal values 0 through 3.
            # Combo operand 4 represents the value of register A.
            # Combo operand 5 represents the value of register B.
            # Combo operand 6 represents the value of register C.
            # Combo operand 7 is reserved and will not appear in valid programs.

            value = None
            match operand:
                case 0: value = 0
                case 1: value = 1
                case 2: value = 2
                case 3: value = 3
                case 4: value = self.registers['A']
                case 5: value = self.registers['B']
                case 6: value = self.registers['C']
                case _: raise ValueError(f"Invalid combo operand: {operand}")

            return value

        def run_one_instruction(self):
            assert self.pc >= 0
            assert self.pc < len(self.program_ints) -1 
            assert self.pc % 2 == 0
            instruction = self.program_ints[self.pc]
            operand     = self.program_ints[self.pc+1]

            # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2**2); an operand of 5 would divide A by 2**8.) The result of the division operation is truncated to an integer and then written to the A register.

            # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

            # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

            # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

            # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

            # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

            # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

            # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

            output = None

            match instruction:
                case 0: # adv
                    numerator = self.registers['A']
                    denominator = 2 ** self.get_combo_operand(operand)
                    result = numerator // denominator
                    self.registers['A'] = result
                    self.pc += 2
                case 1: # bxl
                    result = self.registers['B'] ^ operand
                    self.registers['B'] = result
                    self.pc += 2
                case 2: # bst
                    value = self.get_combo_operand(operand) % 8
                    self.registers['B'] = value
                    self.pc += 2
                case 3: # jnz
                    if self.registers['A'] != 0:
                        self.pc = operand
                    else:
                        self.pc += 2
                case 4: # bxc
                    result = self.registers['B'] ^ self.registers['C']
                    self.registers['B'] = result
                    self.pc += 2
                case 5: # out
                    value = self.get_combo_operand(operand) % 8
                    self.pc += 2
                    output = value
                    self.output_ints.append(value)
                case 6: # bdv
                    numerator = self.registers['A']
                    denominator = 2 ** self.get_combo_operand(operand)
                    result = numerator // denominator
                    self.registers['B'] = result
                    self.pc += 2
                case 7: # cdv
                    numerator = self.registers['A']
                    denominator = 2 ** self.get_combo_operand(operand)
                    result = numerator // denominator
                    self.registers['C'] = result
                    self.pc += 2
                case _: raise ValueError(f"Invalid instruction: {instruction}")

            return output
       
        def get_program_ints_csv(self):
            return self.program_ints_csv

        def set_register( self, label, value ):
            assert label in self.registers
            assert isinstance(value, int)
            assert value >= 0

            self.registers[label] = value

    known_contexts = set()

    def recurse_through_outputs_and_as(
            spec                        :dict, 
            correct_output_ints_so_far  :list[int]=[], 
            a_ints_so_far               :list[int]=[] 
            ):
        """
        return best_a:int (or None)
        """

        context = hash( (','.join(map(str, correct_output_ints_so_far)), ','.join(map(str, a_ints_so_far))))
        if context in known_contexts:
            return None
        else:
            known_contexts.add( context )

        computer = Computer(spec)
        target_output = computer.program_ints_csv
        target_output_ints = computer.program_ints

        assert len(target_output_ints)>=len(correct_output_ints_so_far)

        # construct lower_a and num_lower_a_bits from a_ints_so_far
        lower_a = 0
        num_lower_a_bits = 0
        for ai in a_ints_so_far:
            lower_a += ai * 2**num_lower_a_bits
            num_lower_a_bits += 3

        # print( f"DEBUG: correct_output_ints_so_far={correct_output_ints_so_far}, a_ints_so_far={a_ints_so_far}, lower_a={lower_a}, num_lower_a_bits={num_lower_a_bits}")

        # iterate over increasing higher_a to find next output char
        best_a = None

        for higher_a in range(0, 2**10):
            a = lower_a + (2**num_lower_a_bits)*higher_a
            computer.reset()
            computer.set_register('A', a)
            output_after_halting_csv, step, output_ints, state = computer.run_until_halting_or_deviates(target_output)

            if state=="HALTED":
                # if a==117440:
                #     print(f"DEBUG: a={a}, higher_a={higher_a}, a_ints_so_far={a_ints_so_far}, num_lower_a_bits={num_lower_a_bits}, output_after_halting_csv={output_after_halting_csv}, target_output={target_output}, output_after_halting_csv==target_output ={output_after_halting_csv==target_output}, step={step}, output_ints={output_ints}, state={state}, best_a={best_a}")
                #     assert False

                if output_after_halting_csv==target_output: # NB might HALT short of full output
                    if best_a == None or a < best_a:
                        best_a = a

            elif state == "DEVIATED":
                # which means final int of output_ints is wrong
                output_ints.pop()

                if len(output_ints) > len(correct_output_ints_so_far):
                    next_correct_output_int = output_ints[len(correct_output_ints_so_far)]
                    next_a_int = higher_a % 2**3

                    recursed_a = recurse_through_outputs_and_as(
                        spec, 
                        correct_output_ints_so_far + [next_correct_output_int],
                        a_ints_so_far + [next_a_int] 
                        )
                    
                    if recursed_a != None:
                        if best_a == None or recursed_a < best_a:
                            best_a = recursed_a
            elif state == "MAXED":
                pass
            else:
                assert False, f"unknown state={state}"

        # print(f"DEBUG: best_a={best_a}")

        return best_a

    output_after_halting_csv = None
    spec = parse_input_into_spec( instance['input'] )
    correct_A = None
    computer = Computer(spec)

    if not 'decorrupt_register_A' in instance:
        output_after_halting_csv = computer.run_until_halting()
    else: 
        target_output = computer.program_ints_csv
        print( f"target_output={target_output}" )

        best_a = recurse_through_outputs_and_as( spec )
        assert best_a != None, "found no valid a"

        # check best_a works
        computer.set_register('A', best_a)
        output_after_halting_csv, step, output_ints, state = computer.run_until_halting_or_deviates(target_output)
        assert state == "HALTED"

        correct_A = best_a

    return {
        'output_after_halting_csv': output_after_halting_csv,
        'correct_A': correct_A,
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

# AOC 2024: 2024-12-31: day17/puzzle2/..
# target_output=0,3,5,4,3,0
# target_output=2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0
# [{'elapsed_time_s': 0.2881907499395311},
#  {'correct_A': 164278899142333,
#   'output_after_halting_csv': '2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0',
#   'elapsed_time_s': 6.307547958800569}]