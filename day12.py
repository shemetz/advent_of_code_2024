from typing import Tuple, Set, Dict
import heapq

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

Position = Tuple[int, int]

width, height = len(input_lines[0]), len(input_lines)
regions: Dict[Position, int] = {}
visited: Set[Position] = set()
answer_1 = 0
answer_2 = 0
for row in range(height):
    for col in range(width):
        if (row, col) not in visited:
            visited.add((row, col))
            cell = input_lines[row][col]
            in_region = {(row, col)}
            queue = [(row, col)]
            while queue:
                r, c = queue.pop(0)
                for dr, dc in ((+1, 0), (-1, 0), (0, +1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < height and 0 <= nc < width):
                        continue
                    if (nr, nc) in visited:
                        continue
                    if input_lines[nr][nc] != cell:
                        continue
                    visited.add((nr, nc))
                    in_region.add((nr, nc))
                    queue.append((nr, nc))
            area = len(in_region)
            perimeter = 0
            for r, c in in_region:
                for dr, dc in ((+1, 0), (-1, 0), (0, +1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in in_region:
                        perimeter += 1
            answer_1 += area * perimeter

            counters_per_side = [0, 0, 0, 0]
            up_sides_seen = set()
            down_sides_seen = set()
            left_sides_seen = set()
            right_sides_seen = set()
            for r, c in in_region:
                for nr, seen, counter_idx in (
                        (r - 1, up_sides_seen, 0),
                        (r + 1, down_sides_seen, 1),
                ):
                    if (nr, c) not in in_region:
                        seen.add((nr, c))
                        counters_per_side[counter_idx] += 1
                        if (nr, c - 1) in seen:
                            counters_per_side[counter_idx] -= 1
                        if (nr, c + 1) in seen:
                            counters_per_side[counter_idx] -= 1
                for nc, seen, counter_idx in (
                        (c - 1, left_sides_seen, 2),
                        (c + 1, right_sides_seen, 3),
                ):
                    if (r, nc) not in in_region:
                        seen.add((r, nc))
                        counters_per_side[counter_idx] += 1
                        if (r - 1, nc) in seen:
                            counters_per_side[counter_idx] -= 1
                        if (r + 1, nc) in seen:
                            counters_per_side[counter_idx] -= 1
            sides = sum(counters_per_side)
            answer_2 += area * sides

print("Answer 1:", answer_1)  # 1377008
print("Answer 2:", answer_2)  # 815788
