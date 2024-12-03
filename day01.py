with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

left, right = [], []
for line in input_lines:
    l, *_, r = line.split(" ")
    left.append(int(l))
    right.append(int(r))

answer_1 = sum(
    abs(l - r) for l, r in zip(sorted(left), sorted(right))
)
print(answer_1)  # 1222801

answer_2 = sum(
    l * sum(1 if l == r else 0 for r in right) for l in left
)

print(answer_2)  # 22545250
