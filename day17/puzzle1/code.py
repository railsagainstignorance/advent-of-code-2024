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
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0''',
    'output_after_halting_csv': '4,6,3,5,6,3,5,2,1,0'
    },    
    {
        'input': "../puzzle1/input.txt",
    },
]

attrs = [
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
            self.registers = spec['registers']
            self.program_ints = spec['program_ints']
            self.pc = 0
            self.output_ints = []
        
        def get_output_as_csv(self):
            return ','.join(map(str, self.output_ints))

        def run_until_halting(self):
            while True:
                if self.pc < 0 or self.pc >= len(self.program_ints):
                    break
                self.run_one_instruction()
            output = self.get_output_as_csv()
            return output
        
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
            instruction = self.program_ints[self.pc]
            operand     = self.program_ints[self.pc+1]

            # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

            # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

            # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

            # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

            # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

            # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

            # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

            # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

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

    spec = parse_input_into_spec( instance['input'] )

    computer = Computer(spec)
    output_after_halting_csv = computer.run_until_halting()

    return {
        'output_after_halting_csv': output_after_halting_csv,
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

# AOC 2024: 2024-12-24: day17/puzzle1/..
# [{'elapsed_time_s': 0.00013816705904901028},
#  {'output_after_halting_csv': '7,5,4,3,4,5,3,4,6',
#   'elapsed_time_s': 0.0008791249711066484}]