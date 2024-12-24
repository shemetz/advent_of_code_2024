import functools
from typing import Dict, Tuple, List

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

"""
example "steps" for example door code (029A):
<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
v<<A>>^A<A>AvA<^AA>A<vAAA>^A
<A^A>^^AvvvA
029A
"""

Coord = Tuple[int, int]

# working with +x = right, +y = down
DIRECTIONS = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0)
}
INV_DIRECTIONS = {
    (0, -1): "^",
    (0, 1): "v",
    (-1, 0): "<",
    (1, 0): ">"
}

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
KEYPAD_COORDS = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "DEADLY_EMPTINESS": (0, 3),
    "0": (1, 3),
    "A": (2, 3),  # (initial coord)
}

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

"""
DIRECTIONAL_PAD_COORDS = {
    "DEADLY_EMPTINESS": (0, 0),
    "^": (1, 0),
    "A": (2, 0),  # (initial coord)
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

KEY_PAD_IDX = 0
DIR_PAD_IDX = 1
PADS_BY_INDEX = [KEYPAD_COORDS, DIRECTIONAL_PAD_COORDS]

# ATTEMPT 1

# # we need to come up with:
# # 1. door_code_path = path to type door code
# # 2. door_code_path_path = path to type door_code_path
# # 3. door_code_path_path_path = path to type door_code_path_path
# #
# def chart_meta_sequence(pad: Dict[str, Tuple[int, int]], target_sequence: str) -> str:
#     sequence = ""
#     curr_coords = pad["A"]
#     for char in target_sequence:
#         target_coords = pad[char]
#         # need to move from curr_coords to target_coords
#         while curr_coords != target_coords:
#             # move in the direction of the digit
#             cx, cy = curr_coords
#             tx, ty = target_coords
#             # NOTE:  must not pass through deadly empty spot!  (0, 3)
#             # PRIORITY ORDER:  right, down, up, left
#             if cx < tx:  # move right
#                 sequence += ">"
#                 curr_coords = (cx + 1, cy)
#             elif cy < ty:  # move down
#                 sequence += "v"
#                 curr_coords = (cx, cy + 1)
#             elif cy > ty:  # move up
#                 sequence += "^"
#                 curr_coords = (cx, cy - 1)
#             elif cx > tx:  # move left
#                 sequence += "<"
#                 curr_coords = (cx - 1, cy)
#         else: # click
#             sequence += "A"
#     return sequence
#
# def solve_and_calc_complexity(dcode: str, inbetween_steps: int):
#     sequence = chart_meta_sequence(KEYPAD_COORDS, dcode)
#     for step in range(inbetween_steps):
#         sequence = chart_meta_sequence(DIRECTIONAL_PAD_COORDS, sequence)
#     number_in_door_code = int(dcode[:-1])
#     # print(len(door_code_path_path_path), door_code_path_path_path)
#     return len(sequence) * number_in_door_code

# should_be:
# <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# is:
# v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A
#
# the "expected" is LEFT LEFT UP UP
# but we do UP UP LEFT LEFT
#
#
# expected:
# <vA  <A  A  >>^A  A        vA  <^A  >A  A        vA  ^A
# -> v<<AA  >^AA  >A
# -> <<^^A
# -> 7
# actual:
# v<<A  >>^A  A        v<A  <A  >>^A  A        vA  A  ^<A  >A
# -> <AA  v<AA  >>^A
# -> ^^<<A
# -> 7


# ATTEMPT #2


@functools.lru_cache(maxsize=None)
def chart_one_step_options(pad_idx: int, start: Coord, end: Coord) -> Tuple[str, ...]:
    if start == end:
        return ("A",)
    sx, sy = start
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    horizontal_moves = ">" * dx if dx > 0 else "<" * (dx * -1) if dx < 0 else ""
    vertical_moves = "v" * dy if dy > 0 else "^" * (dy * -1) if dy < 0 else ""
    h_v_sequence = horizontal_moves + vertical_moves + "A"
    v_h_sequence = vertical_moves + horizontal_moves + "A"
    if h_v_sequence == v_h_sequence:
        return (h_v_sequence,)  # just a single direction
    # drop sequence with deadly emptiness
    if pad_idx == DIR_PAD_IDX and sx == 0 and ey == 0:
        return (h_v_sequence,)  # >^
    if pad_idx == DIR_PAD_IDX and sy == 0 and ex == 0:
        return (v_h_sequence,)  # v<
    if pad_idx == KEY_PAD_IDX and sx == 0 and ey == 3:
        return (h_v_sequence,)  # >v
    if pad_idx == KEY_PAD_IDX and sy == 3 and ex == 0:
        return (v_h_sequence,)  # ^<
    return h_v_sequence, v_h_sequence


@functools.lru_cache(maxsize=None)
def chart_meta_sequence_options(pad_idx: int, target_sequence: str) -> Tuple[str, ...]:
    pad = PADS_BY_INDEX[pad_idx]
    options = [""]
    curr_coords = pad["A"]
    for char in target_sequence:
        target_coords = pad[char]
        sequences = chart_one_step_options(pad_idx, curr_coords, target_coords)
        if len(sequences) == 1:
            options = [option + sequences[0] for option in options]
        else:  # len = 2
            options = [option + sequences[0] for option in options] + [option + sequences[1] for option in options]
        curr_coords = target_coords
    return tuple(options)


def solve_and_calc_complexity(dcode: str, inbetween_steps: int):
    options = chart_meta_sequence_options(KEY_PAD_IDX, dcode)
    for step in range(inbetween_steps):
        next_options = []
        for option in options:
            sub_options = chart_meta_sequence_options(DIR_PAD_IDX, option)
            next_options.extend(sub_options)
        shortest_option_length = min(len(option) for option in next_options)
        options = [option for option in next_options if len(option) == shortest_option_length]
    # select shortest option
    shortest_option = min(options, key=len)
    number_in_door_code = int(dcode[:-1])
    return len(shortest_option) * number_in_door_code

answer_1 = 0
answer_2 = 0
for line in input_lines:
    answer_1 += solve_and_calc_complexity(line, 2)
    answer_2 += solve_and_calc_complexity(line, 25)



print("Answer 1:", answer_1)  # 215374
print("Answer 2:", answer_2)  #
