with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

answer_1 = 0
for line in input_lines:
    levels = [int(x) for x in line.split(' ')]
    if sorted(levels) == levels or sorted(levels, reverse=True) == levels:
        if all(1 <= abs(x1 - x2) <= 3 for x1, x2 in zip(levels, levels[1:])):
            answer_1 += 1

print("Answer 1:", answer_1)  # 341

answer_2 = 0
for line in input_lines:
    levels = [int(x) for x in line.split(' ')]
    for i in range(-1, len(levels)):
        l_copy = levels.copy()
        if i != -1:
            l_copy.pop(i)
        if sorted(l_copy) == l_copy or sorted(l_copy, reverse=True) == l_copy:
            if all(1 <= abs(x1 - x2) <= 3 for x1, x2 in zip(l_copy, l_copy[1:])):
                answer_2 += 1
                break

print("Answer 2:", answer_2)  # 404
