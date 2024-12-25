from collections import defaultdict
from typing import List, Set, Tuple, Dict

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

width = len(input_lines[0])
height = len(input_lines)
start = 0
# start facing up (1 row up)
# (reminder:  in my complex numbers grids, 1j is down and multiplying by 1j is turning right)
start_dir = -1j
walls: Set[complex] = set()
for row, line in enumerate(input_lines):
    for col, char in enumerate(line):
        if char == '#':
            walls.add(row * 1j + col)
        if char == "^":
            start = row * 1j + col

# part 1
visited_counts_1: Dict[complex, int] = defaultdict(lambda: 0)
visited_counts_1[start] = 1
position = start
direction = start_dir
while 0 <= position.real < width and 0 <= position.imag < height:
    next_position = position + direction
    if next_position in walls:
        # turn right
        direction = direction * 1j
        next_position = position + direction
    else:
        position = next_position
        visited_counts_1[position] += 1
answer_1 = len(visited_counts_1)  # number of unique visited positions, ignores the counts for now
print("Answer 1:", answer_1)  # 4559

# part 2
answer_2 = 0
# memoization:  shortcuts, keeping track of only turning points
memo: Dict[Tuple[complex, complex], Tuple[complex, complex]] = {}
last_turn = (start, start_dir)
for block_r in range(height):
    for block_c in range(width):
        block = block_r * 1j + block_c
        if block not in visited_counts_1:
            continue
        # try inserting the block and seeing if it results in a loop
        did_loop = False
        visited_counts = defaultdict(lambda: 0)
        visited_counts[start] = 1
        position = start
        direction = start_dir
        while 0 <= position.real < width and 0 <= position.imag < height:
            if (position, direction) in memo and block.real != position.real and block.imag != position.imag:
                # shortcut
                position, direction = memo[(position, direction)]
                continue
            next_position = position + direction
            if next_position in walls or next_position == block:
                if next_position != block:
                    memo[(position, direction)] = last_turn
                # turn right
                direction = direction * 1j
                next_position = position + direction
                last_turn = (next_position, direction)
            else:
                position = next_position
                visited_counts[position] += 1
                if visited_counts[position] > 4:  # this extra safety margin is crucial ¯\_(ツ)_/¯
                    did_loop = True
                    break
        if did_loop:
            answer_2 += 1
print("Answer 2:", answer_2)  # 1604
