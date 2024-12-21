from typing import Set, List, Tuple, Dict

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

Row = int
Col = int
Height = int
Position = Tuple[Row, Col]

grid: List[List[Height]] = []
for line in input_lines:
    grid.append([int(c) for c in line])
g_height = len(grid)
g_width = len(grid[0])

answer_1 = 0
answer_2 = 0
for row in range(g_height):
    for col in range(g_width):
        trailhead = grid[row][col]
        if trailhead == 0:
            score = 0
            rating = 0
            visit_counters: Dict[Position, int] = { (row, col): 1 }
            queue = [(row, col)]
            while queue:
                r, c = queue.pop(0)
                if grid[r][c] == 9:
                    score += 1
                    rating += visit_counters[(r, c)]
                    continue
                for dr, dc in ((+1, 0), (-1, 0), (0, +1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < g_height and 0 <= nc < g_width):
                        continue
                    if grid[nr][nc] != grid[r][c] + 1:
                        continue
                    if (nr, nc) in visit_counters:
                        visit_counters[(nr, nc)] += visit_counters[(r, c)]
                        continue
                    visit_counters[(nr, nc)] = visit_counters[(r, c)]
                    queue.append((nr, nc))
            answer_1 += score
            answer_2 += rating
print("Answer 1:", answer_1)  # 430
print("Answer 2:", answer_2)  # 928
