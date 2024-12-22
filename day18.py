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
    queue = [(start_pos, (start_pos,))]
    while queue:
        pos, path = queue.pop(0)
        if pos == end_pos:
            return path
        if pos in visited:
            continue
        visited.add(pos)
        for move in [1, -1, 1j, -1j]:
            new_pos = pos + move
            if not (0 <= new_pos.real < SIZE_PART_1 and 0 <= new_pos.imag < SIZE_PART_1):
                continue
            if new_pos in walls or new_pos in visited:
                continue
            queue.append((new_pos, path + (new_pos,)))
    return None


last_path = tuple()
for t, line in enumerate(input_lines):
    xs, ys = re.findall(r'-?\d+', line)
    x, y = int(xs), int(ys)
    wall = complex(x, y)
    walls.add(wall)
    if t == SIMULATED_NUM_FOR_PART_1 - 1:
        last_path = pathfind()
        answer_1 = len(last_path) - 1
        print("Answer 1", answer_1)  # 262
    if wall in last_path:  # only recalculate when a wall obstructs the previous path!
        path = pathfind()
        if path is None:
            print("Answer 2", line)  # 22,20
            break
        last_path = path
