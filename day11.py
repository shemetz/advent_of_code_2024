from collections import defaultdict
from typing import Set, List, Tuple, Dict

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

stones: Dict[int, int] = {}
for num in input_lines[0].split(" "):
    stones[int(num)] = stones.get(int(num), 0) + 1

answer_1, answer_2 = None, None
for i in range(75):
    next_stones = defaultdict(lambda: 0)
    for num in stones:
        len_str_num = len(str(num))
        if num == 0:
            next_stones[1] += stones[num]
        elif len_str_num % 2 == 0:
            left = int(str(num)[:len_str_num // 2])
            right = int(str(num)[len_str_num // 2:])
            next_stones[left] += stones[num]
            next_stones[right] += stones[num]
        else:
            next_stones[num * 2024] += stones[num]
    stones = next_stones
    if i == 25 - 1:
        answer_1 = sum(stones.values())
    if i == 75 - 1:
        answer_2 = sum(stones.values())

print("Answer 1:", answer_1)  # 194782
print("Answer 2:", answer_2)  # 233007586663131
