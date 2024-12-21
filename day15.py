from typing import List, Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

EMPTY = '.'
WALL = '#'
ME = '@'
SIMPLE_BLOCK = 'O'
LEFT_BLOCK = '['
RIGHT_BLOCK = ']'
DIR_UP = (-1, 0)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)
DIR_RIGHT = (0, 1)
DIRS_BY_CHAR = {
    '^': DIR_UP,
    '>': DIR_RIGHT,
    'v': DIR_DOWN,
    '<': DIR_LEFT,
}

Point = Tuple[int, int]
Direction = Tuple[int, int]
Grid = List[List[str]]
MoveDirs = List[Direction]


def make_grid(part: int):
    player_start: Point = (-1, -1)
    grid: Grid = []
    move_dirs: MoveDirs = []
    for row, line in enumerate(input_lines):
        grid.append([])
        if line.startswith("#"):
            for col, c in enumerate(line):
                if part == 1:
                    if c == ME:
                        player_start = (row, col)
                        grid[-1].append(EMPTY)
                    else:
                        grid[-1].append(c)
                if part == 2:
                    if c == ME:
                        player_start = (row, col * 2)
                        grid[-1].append(EMPTY)
                        grid[-1].append(EMPTY)
                    elif c in [EMPTY, WALL]:
                        grid[-1].append(c)
                        grid[-1].append(c)
                    else:
                        grid[-1].append(LEFT_BLOCK)
                        grid[-1].append(RIGHT_BLOCK)
        elif line == "":
            continue
        else:
            for c in line:
                move_dirs.append(DIRS_BY_CHAR[c])
    return player_start, grid, move_dirs


def check_if_can_move(grid: Grid, from_row: int, from_col: int, direction: Direction):
    row, col = from_row + direction[0], from_col + direction[1]
    cell = grid[row][col]
    if cell == EMPTY:
        return True
    if cell == WALL:
        return False
    if cell == SIMPLE_BLOCK or \
            (cell in (LEFT_BLOCK, RIGHT_BLOCK) and direction in (DIR_LEFT, DIR_RIGHT)):
        # horizontal movement only recurses once
        return check_if_can_move(grid, row, col, direction)
    else:
        # = cell is LEFT/RIGHT and being pushed UP/DOWN, so vertical movement
        if direction == DIR_UP or direction == DIR_DOWN:
            # pushing one side pushing the entire block, so now we recurse twice
            other_side = col + 1 if cell == LEFT_BLOCK else col - 1
            return \
                    check_if_can_move(grid, row, col, direction) and \
                    check_if_can_move(grid, row, other_side, direction)
    raise ValueError(f"Unexpected cell type: {cell}")


def actually_move(grid: Grid, from_row: int, from_col: int, direction: Direction):
    from_cell = grid[from_row][from_col]
    row, col = from_row + direction[0], from_col + direction[1]
    cell = grid[row][col]

    grid[from_row][from_col] = EMPTY
    if cell == EMPTY:
        pass
    elif cell == SIMPLE_BLOCK or \
            (cell in (LEFT_BLOCK, RIGHT_BLOCK) and direction in (DIR_LEFT, DIR_RIGHT)):
        # horizontal movement only recurses once
        actually_move(grid, row, col, direction)
    else:
        # = cell is LEFT/RIGHT and being pushed UP/DOWN, so vertical movement
        if direction == DIR_UP or direction == DIR_DOWN:
            # pushing one side pushing the entire block, so now we recurse twice
            other_side = col + 1 if cell == LEFT_BLOCK else col - 1
            actually_move(grid, row, col, direction)
            actually_move(grid, row, other_side, direction)
    grid[row][col] = from_cell
    return grid


def print_grid(grid: Grid, player_pos: Point):
    for row, line in enumerate(grid):
        for col, c in enumerate(line):
            if (row, col) == player_pos:
                print(ME, end="")
            else:
                print(c, end="")
        print()


def solve_part(part: int):
    me, grid, move_dirs = make_grid(part)
    for direction in move_dirs:
        if not check_if_can_move(grid, me[0], me[1], direction):
            continue
        grid = actually_move(grid, me[0], me[1], direction)
        me = me[0] + direction[0], me[1] + direction[1]
    # print_grid(grid, me)
    answer = 0
    for row, line in enumerate(grid):
        for col, c in enumerate(line):
            if c in [SIMPLE_BLOCK, LEFT_BLOCK]:
                answer += 100 * row + col
    return answer


answer_1 = solve_part(1)
print("Answer 1:", answer_1)  # 1294459

# Part 2

answer_2 = solve_part(2)
print("Answer 2:", answer_2)  # 1319212
