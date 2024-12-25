import itertools
from typing import Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

HeightsTuple = Tuple[int, int, int, int, int]
keys = []
locks = []
for i in range((len(input_lines) + 1) // 8):
    seven_lines = input_lines[i * 8: (i + 1) * 8 - 1]
    count = lambda x: sum(1 for line in seven_lines if line[x] == "#") - 1
    heights = (count(0), count(1), count(2), count(3), count(4))
    is_lock = seven_lines[0][0] == "#"
    (locks if is_lock else keys).append(heights)

answer_1 = 0
for key, lock in itertools.product(keys, locks):
    if all(k + l < 6 for k, l in zip(key, lock)):
        answer_1 += 1


print("Answer 1", answer_1)  # 2933
print("Answer 2", 0)  #
