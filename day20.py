import heapq
from collections import defaultdict
from itertools import combinations
from typing import Dict, Tuple, List

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

MIN_IMPROVEMENT = 100
# MIN_IMPROVEMENT = 12
# MIN_IMPROVEMENT = 72

board_size = len(input_lines)
normal_score_no_cheats = board_size ** 2 - 1  # S is not counted
Pos2D = Tuple[int, int]
board: Dict[Pos2D, str] = {}
start_pos, end_pos = (0, 0), (0, 0)  # just for type safety
for r, line in enumerate(input_lines):
    for c, char in enumerate(line):
        board[(r, c)] = char
        if char == "S":
            start_pos = (r, c)
        if char == "E":
            end_pos = (r, c)
        if char == "#":
            normal_score_no_cheats -= 1
max_path_length = normal_score_no_cheats - MIN_IMPROVEMENT

normal_path: List[Tuple[Pos2D, int, int]] = []  # position, distance from start, distance to end
visited = {start_pos}
normal_path.append((start_pos, 0, normal_score_no_cheats))
while normal_path[-1][0] != end_pos:
    pos, d_from_s, d_to_e = normal_path[-1]
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_pos = (pos[0] + dr, pos[1] + dc)
        if next_pos in visited:
            continue
        if board.get(next_pos, '#') == '#':
            continue
        visited.add(next_pos)
        normal_path.append((next_pos, d_from_s + 1, d_to_e - 1))
        break  # because normal map is labyrinth

answer_1 = 0
answer_2 = 0
for it1, it2 in combinations(normal_path, 2):
    pos1, ds1, de1 = it1
    pos2, ds2, de2 = it2
    abs_dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    if abs_dist == 2 and ds1 + abs_dist + de2 <= max_path_length:
        answer_1 += 1
    if 1 <= abs_dist <= 20 and ds1 + abs_dist + de2 <= max_path_length:
        answer_2 += 1

print("Answer 1:", answer_1)  # 1502
print("Answer 2:", answer_2)  # 1028136
