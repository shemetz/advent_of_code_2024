import re

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

answer_1 = 0
for line in input_lines:
    muls = re.findall(r"mul\((\d+),(\d+)\)", line)
    for mul in muls:
        answer_1 += int(mul[0]) * int(mul[1])

print("Answer 1:", answer_1)  # 167090022



answer_2 = 0
enabled = True # (note:  this is set just once, not once per line!)
for line in input_lines:
    cmds = re.findall(r"mul\((\d+),(\d+)\)|(do)\(\)|(don)'t\(\)", line)
    for cmd in cmds:
        if cmd[2] == "do":
            enabled = True
        elif cmd[3] == "don":
            enabled = False
        else:
            if enabled:
                answer_2 += int(cmd[0]) * int(cmd[1])

print("Answer 2:", answer_2)  # 89823704
