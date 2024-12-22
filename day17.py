from functools import lru_cache
from typing import Tuple, Set, Dict

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

"""
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

initial_registers = (
    int(input_lines[0].split(": ")[1]),
    int(input_lines[1].split(": ")[1]),
    int(input_lines[2].split(": ")[1]),
)
program_raw = input_lines[4].split(": ")[1]
program = [int(x) for x in program_raw.split(",")]

format1 = lambda x: bin(x).replace("0b", "").rjust(30)
format2 = lambda x: bin(x & 0b111).replace("0b", "").rjust(3, "0").rjust(6)
format3 = lambda x: oct(x).replace("0o", "").rjust(17, "0")
format4 = lambda x: oct(x).replace("0o", "").rjust(4, "0")
cache = {}


def run_program(registers: Tuple[int, int, int], part: int):
    ip = 0  # instruction pointer
    reg_a, reg_b, reg_c = registers
    output = []
    while 0 <= ip < len(program) - 1:
        next_ip = ip + 2
        instr = program[ip]
        literal = program[ip + 1]
        combo = -1
        if literal <= 3:
            combo = literal
        elif literal == 4:
            combo = reg_a
        elif literal == 5:
            combo = reg_b
        elif literal == 6:
            combo = reg_c
        elif literal == 7:
            combo = -9999

        if instr == 0:  # adv, divide register A by 2^combo
            reg_a = reg_a // (2 ** combo)
        elif instr == 1:  # bxl, xor reg B with literal
            reg_b = reg_b ^ literal
        elif instr == 2:  # bst, regB = combo modulo 8
            reg_b = combo % 8
        elif instr == 3:  # jnz, jump if reg A is not 0
            if reg_a != 0:
                next_ip = literal
        elif instr == 4:  # bxc, xor reg B with reg C.  "For legacy reasons, this instruction reads an operand but ignores it."
            reg_b = reg_b ^ reg_c
        elif instr == 5:  # out, output combo mod 8
            output.append(combo % 8)
            if part == 2:
                if not program_raw.startswith(",".join(str(x) for x in output)):
                    return None
        elif instr == 6:  # bdv, divide reg B by 2^combo
            reg_b = reg_a // (2 ** combo)
        elif instr == 7:  # cdv, divide reg C by 2^combo
            reg_c = reg_a // (2 ** combo)
        else:
            raise ValueError(f"Invalid instruction {instr}")
        ip = next_ip
        # print(format1(ip), format1(reg_a), format2(reg_b), format2(reg_c))
    return ",".join(str(x) for x in output)


answer_1 = run_program(tuple(initial_registers), 1)
print("Answer 1:", answer_1)  # 1,4,6,1,6,4,3,0,3


def run_program_optimized(initial_reg_a):
    """
    my code is:
    >>> 2,4, 1,7, 7,5, 1,7, 4,6, 0,3, 5,5, 3,0
    =
    0. (regA = [some_high_number])         # e.g. 0o11011101

    1. (2,4) reg_b = reg_a % 8             # reg_b is now e.g. 0b101
    2. (1,7) reg_b = reg_b ^ 7             # reg_b is now e.g. 0b010
    3. (7,5) reg_c = reg_a // 2**reg_b     # reg_c is now e.g. 0b01101100  # =shifted version of reg_a right by reg_b
    4. (1,7) reg_b = reg_b ^ 7             # reg_b is now e.g. 0b101 again
    5. (4,6) reg_b = reg_b ^ reg_c         # reg_b is now e.g. 0b000

    6. (0,3) reg_a = reg_a // 2**3         # reg_a is now e.g. 0b00011011  # =shifted version of reg_a right by 3
    7. (5,5) output reg_b % 8              # output e.g. 0
    8. (3,0) jump to 0 if reg_a != 0       # loop back to step 0

    written in code, a bit simpler:
    >>> while reg_a > 0:
    ...     reg_a = 0b11111100101101010000100001     # some_high_number
    ...     reg_c = reg_a >> ((reg_a & 0b111) ^ 7)
    ...     reg_b = (reg_a & 0b111) ^ reg_c          # =
    ...     print(reg_b & 0b111)                     # output the three bits
    ...     reg_a = reg_a >> 3

    I'm not sure what this does exactly, some shit about XORing the rightmost 3 bits of regA with the ???thmost 3 bits
     of A again and again.
    """

    reg_a = initial_reg_a
    output = []
    while reg_a > 0:
        reg_c = reg_a >> ((reg_a & 0b111) ^ 7)
        reg_b = (reg_a & 0b111) ^ reg_c
        output.append(reg_b & 0b111)
        reg_a = reg_a >> 3
    return ",".join(str(x) for x in output)


@lru_cache
def run_program_optimized_cached(initial_reg_a):
    """
    but I know enough to see that I can memoize everything based only on reg_a and ip!
    """
    if initial_reg_a == 0:
        return ""
    reg_a = initial_reg_a
    reg_c = reg_a >> ((reg_a & 0b111) ^ 7)
    reg_b = (reg_a & 0b111) ^ reg_c
    left = reg_b & 0b111
    right = run_program_optimized_cached(reg_a >> 3)
    return str(left) + ("," + right if len(right) else "")


# answer_2 = answer_1
# for i in range(1, 0o777777777777777777777):
#     attempt_output = run_program_optimized_cached(i)
#     if i % 10_000_000 == 0:
#         print("i =", i, "output", attempt_output)
#     if attempt_output == program_raw:
#         answer_2 = i
#         break
# print("Answer 2:", answer_2)  #

# ...manual attempts
# goal:   2,4,1,7,7,5,1,7,4,6,0,3,5,5,3,0 .
# here's my code halfway through:
# for i in range(0, 0o7777 + 1):
#     inp = 0o1000000000000_2621633 + (i << 3*7)
#     attempt_output = run_program_optimized(inp)
#     print(format3(inp), format4(i), "->", attempt_output)

# 0o00073006255136621633    almost but not quite!  (extra 0 at the end)

# ...manual attempts continue...
# for i in range(0, 0o1000):
#     inp = 0o_742_111_503_662_100_0 + i
#     attempt_output = run_program_optimized(inp)
#     print(format3(inp), format4(i), "->", attempt_output, ".")
#     if attempt_output == program_raw:
#         print("SUCCESS")
#         print("Answer 2:", inp)
#         break

# 0o7260x... nope
# 0o7421115036621633 yesss!!!   but noooooo
# -> 265061364605851 is too high :(

# # ...manual attempts continue...fine-tuning to get lowest...!
# for i in range(0, 0o1000):
#     inp = 0o0_001_115_036_621_633 + (i << 3*13)
#     attempt_output = run_program_optimized(inp)
#     print(format3(inp), format4(i), "->", attempt_output, ".")
#     if attempt_output == program_raw:
#         print("SUCCESS")
#         print("Answer 2:", inp)
#         break


# just copying and altering a similar nd smarter answer from online:
def step(reg_a):
    reg_c = reg_a >> ((reg_a & 0b111) ^ 7)
    reg_b = (reg_a & 0b111) ^ reg_c
    return reg_b & 0b111


def find(A, index):
    if step(A) != program[index]:
        return

    if index == 0:
        As.append(A)
    else:
        for B in range(8):
            find(A * 8 + B, index - 1)


As = []
first_index = len(program) - 1
for a in range(8):
    find(a, first_index)
print("Answer 2", min(As))  # 265061364597659
