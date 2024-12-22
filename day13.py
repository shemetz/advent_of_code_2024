import z3
import re

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

answer_1 = 0
answer_2 = 0
for i in range((len(input_lines) + 1) // 4):
    a_x_s, a_y_s = re.findall(r"(\d+)", input_lines[i * 4 + 0])
    a_x, a_y = int(a_x_s), int(a_y_s)
    b_x_s, b_y_s = re.findall(r"(\d+)", input_lines[i * 4 + 1])
    b_x, b_y = int(b_x_s), int(b_y_s)
    p_x_s, p_y_s = re.findall(r"(\d+)", input_lines[i * 4 + 2])
    p_x, p_y = int(p_x_s), int(p_y_s)

    a_presses = z3.Int("a_presses")
    b_presses = z3.Int("b_presses")

    s_1 = z3.Solver()
    # a >= 0, or a <= 100... not actually needed here!  but can be easily added
    s_1.add(a_presses * a_x + b_presses * b_x == p_x)
    s_1.add(a_presses * a_y + b_presses * b_y == p_y)
    if s_1.check() == z3.sat:
        m = s_1.model()
        answer_1 += m[a_presses].as_long() * 3 + m[b_presses].as_long() * 1

    s_2 = z3.Solver()
    s_2.add(a_presses * a_x + b_presses * b_x == p_x + 10000000000000)
    s_2.add(a_presses * a_y + b_presses * b_y == p_y + 10000000000000)
    if s_2.check() == z3.sat:
        m = s_2.model()
        answer_2 += m[a_presses].as_long() * 3 + m[b_presses].as_long() * 1

print("Answer 1:", answer_1)  # 37297
print("Answer 2:", answer_2)  # 83197086729371
