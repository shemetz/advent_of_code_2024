import re

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

# SIMULATED_NUM_FOR_PART_1 = 12
# SIZE_PART_1 = 7
SIMULATED_NUM_FOR_PART_1 = 1024
SIZE_PART_1 = 71
start_pos = complex(0, 0)
end_pos = complex(SIZE_PART_1 - 1, SIZE_PART_1 - 1)
walls = set()


def pathfind():
    # simple bfs
    visited = set()
    queue = [(start_pos, 0)]
    while queue:
        pos, steps = queue.pop(0)
        if pos == end_pos:
            return steps
        if pos in visited:
            continue
        visited.add(pos)
        for move in [1, -1, 1j, -1j]:
            new_pos = pos + move
            if not (0 <= new_pos.real < SIZE_PART_1 and 0 <= new_pos.imag < SIZE_PART_1):
                continue
            if new_pos in walls or new_pos in visited:
                continue
            queue.append((new_pos, steps + 1))
    return None


for t, line in enumerate(input_lines):
    xs, ys = re.findall(r'-?\d+', line)
    x, y = int(xs), int(ys)
    walls.add(complex(x, y))
    if t == SIMULATED_NUM_FOR_PART_1 - 1:
        answer_1 = pathfind()
        print("Answer 1", answer_1)  # 262
    path_found = pathfind() is not None
    if not path_found:
        print("Answer 2", line)  # 22,20
        break
