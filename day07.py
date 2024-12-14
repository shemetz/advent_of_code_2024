from functools import lru_cache
from typing import List, Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

equations: List[Tuple[int, Tuple[int, ...]]] = []
for line in input_lines:
    s_goal, rest_after_goal = line.split(": ")
    s_operands = rest_after_goal.split(" ")
    equations.append((int(s_goal), tuple(int(operand) for operand in s_operands)))


@lru_cache
def recursive_try_solving_equation(current: int, goal: int, remaining_operands: Tuple[int, ...], part: int) -> bool:
    if len(remaining_operands) == 0:
        return current == goal
    if current > goal:
        return False  # cannot reach target goal with only + and *;  early exit
    next_operand = remaining_operands[0]
    remaining = tuple(remaining_operands[1:])
    if recursive_try_solving_equation(current + next_operand, goal, remaining, part):
        return True
    if recursive_try_solving_equation(current * next_operand, goal, remaining, part):
        return True
    if part == 2 and recursive_try_solving_equation(int(str(current) + str(next_operand)), goal, remaining, part):
        return True
    return False


answer_1 = 0
for goal_i, operands_i in equations:
    if recursive_try_solving_equation(operands_i[0], goal_i, operands_i[1:], part=1):
        answer_1 += goal_i
print("Answer 1:", answer_1)  # 850435817339

answer_2 = 0
for goal_i, operands_i in equations:
    if recursive_try_solving_equation(operands_i[0], goal_i, operands_i[1:], part=2):
        answer_2 += goal_i
print("Answer 2:", answer_2)  # 104824810233437
