from typing import List

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

rules = set()
updates = []
is_updating = False
for line in input_lines:
    if is_updating:
        updates.append([int(s) for s in line.split(",")])
    elif line == "":
        is_updating = True
    else:
        rules.add(tuple(int(s) for s in line.split("|")))


def is_valid_update(some_update: List[int]) -> bool:
    for idx1, id1 in enumerate(some_update):
        for idx2, id2 in enumerate(some_update[idx1 + 1:]):
            if (id2, id1) in rules:
                return False
    return True


answer_1 = 0
for update in updates:
    if is_valid_update(update):
        answer_1 += update[int((len(update) - 1) / 2)]
print("Answer 1:", answer_1)  # 4924


def fix_update(some_update: List[int]) -> List[int]:
    new_update = []
    for id1 in some_update:
        for pos_before in range(len(new_update) + 1):
            for idx2, id2 in enumerate(new_update):
                if pos_before <= idx2 and (id2, id1) in rules:
                    break  # inserting here would be illegal
                if idx2 < pos_before and (id1, id2) in rules:
                    break  # inserting here would be illegal
            else:  # good position found
                new_update = new_update[:pos_before] + [id1] + new_update[pos_before:]
                break
        else:  # no good position found
            raise ValueError(f"No good position found for {id1} in {new_update}")
    return new_update


answer_2 = 0
for update in updates:
    if not is_valid_update(update):
        fixed_update = fix_update(update)
        answer_2 += fixed_update[int((len(fixed_update) - 1) / 2)]
print("Answer 2:", answer_2)  # 6085
