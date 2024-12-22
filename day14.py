import re
from time import sleep
from typing import List, Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

# HEIGHT = 7
HEIGHT = 103
# WIDTH = 11
WIDTH = 101
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
TIME_TO_WAIT = 100

robots: List[Tuple[complex, complex]] = []
for line in input_lines:
    # e.g. p=0,4 v=3,-3
    numbers = re.findall(r'-?\d+', line)
    pos = complex(int(numbers[0]), int(numbers[1]))
    vel = complex(int(numbers[2]), int(numbers[3]))
    robots.append((pos, vel))

positions = [pos for pos, vel in robots]
for t in range(TIME_TO_WAIT):
    for i in range(len(robots)):
        pos, vel = robots[i]
        positions[i] = positions[i] + vel
        positions[i] = complex(
            int(positions[i].real) % WIDTH,
            int(positions[i].imag) % HEIGHT,
        )

quadrant_counts = [[0, 0], [0, 0]]
for pos in positions:
    if pos.real < CENTER_X and pos.imag < CENTER_Y:
        quadrant_counts[0][0] += 1
    elif pos.real > CENTER_X and pos.imag < CENTER_Y:
        quadrant_counts[0][1] += 1
    elif pos.real < CENTER_X and pos.imag > CENTER_Y:
        quadrant_counts[1][0] += 1
    elif pos.real > CENTER_X and pos.imag > CENTER_Y:
        quadrant_counts[1][1] += 1
answer_1 = quadrant_counts[0][0] * quadrant_counts[0][1] * quadrant_counts[1][0] * quadrant_counts[1][1]
print("Answer 1:", answer_1)  # 226236192

positions = [pos for pos, vel in robots]
for t in range(WIDTH * HEIGHT + 1):
    for i in range(len(robots)):
        pos, vel = robots[i]
        positions[i] = positions[i] + vel
        positions[i] = complex(
            int(positions[i].real) % WIDTH,
            int(positions[i].imag) % HEIGHT,
        )

    search_area_radius = 7
    suspicious = len(set(positions)) == len(robots)

    # if t % 103 == 30:  # suspicious verticals
    # if t % 101 >= 14:  # suspicious horizontals
    if suspicious:
        printed = str(t) + "\n"
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if complex(x, y) in positions:
                    printed += "O"
                else:
                    printed += " "
            printed += "\n"
        printed += str(t) + "\n" * 4
        print(printed)
# MANUAL (look at console)
# SUSPICIOUS verticals:  30, 236,
# SUSPICIOUS horizontals:  390, 693, 1198
# ANSWER - when t = 8167
print("Answer 2:", 8168)  # 8167 + 1
