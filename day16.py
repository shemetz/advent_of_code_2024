from typing import Tuple, Set, Dict
import heapq

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

EMPTY = '.'
WALL = '#'
START = 'S'
END = 'E'

width, height = len(input_lines[0]), len(input_lines)
Position = complex
Direction = complex
Vector = Tuple[Position, Direction]

start_pos: Position = -1
start_dir: Direction = 1
end_pos: Position = -1
walls: Set[Position] = set()
for y, row in enumerate(input_lines):
    for x, cell in enumerate(row):
        if cell == "#":
            walls.add(x + y * 1j)
        elif cell == "S":
            start_pos = x + y * 1j
        elif cell == "E":
            end_pos = x + y * 1j

Price = int  # "price" = score, we are trying to minimize it
HalfwayId = int
Path = Tuple[Position, ...]
Thingie = Tuple[Price, HalfwayId, Position, Direction, Path]  # price, position, direction


def solve_to_get_min_price():
    # dijkstra time!
    seen = set()
    min_price_dict: Dict[Vector, Price] = {(start_pos, start_dir): 0}
    heap = [(0, id((start_pos, start_dir)), start_pos, start_dir, tuple())]
    heapq.heapify(heap)
    while heap:
        price, _id, pos, direc, path = heapq.heappop(heap)
        if (pos, direc) in seen:
            continue
        seen.add((pos, direc))
        if pos == end_pos:
            return price, path
        for new_direc in [direc, direc * 1j, direc * -1j]:
            new_pos = pos + new_direc
            if new_pos in walls:
                continue
            did_turn = new_direc != direc
            if (new_pos, new_direc) in seen:
                continue
            new_price = price + (1001 if did_turn else 1)
            if min_price_dict.get((new_pos, new_direc), 99999999) <= new_price:
                continue
            min_price_dict[(new_pos, new_direc)] = new_price
            new_path = path + (new_pos,)
            heapq.heappush(heap, (new_price, id((new_pos, new_direc)), new_pos, new_direc, new_path))


def print_path(path: Set[Position]):
    for y in range(height):
        for x in range(width):
            pos = x + y * 1j
            if pos in walls:
                print("#", end="")
            elif pos == start_pos:
                print("S", end="")
            elif pos == end_pos:
                print("E", end="")
            elif pos in path:
                print("O", end="")
            else:
                print(".", end="")
        print()


answer_1, path_1 = solve_to_get_min_price()
# print_path(path_1)
# print()
print("Answer 1:", answer_1)  # 103512


# Part 2

def solve_to_find_all_paths_of_price(the_price: int):
    # dijkstra time but with all paths this time!
    seen = set()
    mins_dict: Dict[
        Vector,
        Tuple[Price, Set[Position]]
    ] = {
        (start_pos, start_dir):
            (0, {start_pos}),
    }
    heap = [(0, id((start_pos, start_dir)), start_pos, start_dir, tuple())]
    heapq.heapify(heap)

    while heap:
        price, _id, pos, direc, path = heapq.heappop(heap)
        if (pos, direc) in seen:
            continue
        seen.add((pos, direc))
        if pos == end_pos and price > the_price:
            break
        for new_direc in [direc, direc * 1j, direc * -1j]:
            new_pos = pos + new_direc
            if new_pos in walls:
                continue
            did_turn = new_direc != direc
            if (new_pos, new_direc) in seen:
                continue
            new_price = price + (1001 if did_turn else 1)
            best_price_so_far, from_where_so_far = mins_dict.get((new_pos, new_direc), (99999999999, set()))
            if best_price_so_far < new_price:
                continue
            if best_price_so_far == new_price:
                from_where_so_far.add(pos)
                continue
            mins_dict[(new_pos, new_direc)] = (new_price, {pos})
            new_path = path + (new_pos,)
            heapq.heappush(heap, (new_price, id((new_pos, new_direc)), new_pos, new_direc, new_path))
    positions_in_best_paths = set()
    que = [(end_pos, the_price)]
    # TODO fix something here, which causes at least one wrong and long branch
    while que:
        place, price = que.pop()
        if place in positions_in_best_paths:
            continue
        positions_in_best_paths.add(place)
        for direc in [1, -1, 1j, -1j]:
            from_price, from_origins = mins_dict.get((place, direc), (99999999999, set()))
            if from_price <= price:
                for origin in from_origins:
                    que.append((origin, from_price))
    print_path(positions_in_best_paths)
    return len(positions_in_best_paths)



answer_2 = solve_to_find_all_paths_of_price(answer_1)
print("Answer 2:", answer_2)  # ...NOT 599, too high, 597 too high too
