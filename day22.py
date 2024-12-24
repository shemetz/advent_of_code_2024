from typing import Dict, Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

mix = lambda a, b: a ^ b
prune = lambda a: a % 16777216  # == 2**24


def monkey_hash(num: int) -> int:
    s1 = prune(mix(num * 64, num))
    s2 = prune(mix(s1 // 32, s1))
    s3 = prune(mix(s2 * 2048, s2))
    return s3


answer_1 = 0
for line in input_lines:
    initial_secret = int(line)
    value = initial_secret
    for _ in range(2000):
        value = monkey_hash(value)
    answer_1 += value

print("Answer 1:", answer_1)  # 19877757850

PriceChange = int  # -9 | -8 | ... | 8 | 9
Quadruplet = Tuple[PriceChange, PriceChange, PriceChange, PriceChange]
profit_by_quad: Dict[Quadruplet, int] = {}
for line in input_lines:
    initial_secret = int(line)
    value = initial_secret
    seen_quadruplets = set()
    curr_5_digits = []
    for _ in range(2000):
        value = monkey_hash(value)
        digit = value % 10
        curr_5_digits.append(digit)
        if len(curr_5_digits) > 4:
            d1, d2, d3, d4, d5 = curr_5_digits
            quadruplet: Quadruplet = (
                d2 - d1,
                d3 - d2,
                d4 - d3,
                d5 - d4
            )
            if quadruplet not in seen_quadruplets:
                seen_quadruplets.add(quadruplet)
                profit_til_now = profit_by_quad.get(quadruplet, 0)
                profit_by_quad[quadruplet] = profit_til_now + d5
            curr_5_digits.pop(0)
answer_2 = max(profit_by_quad.values())
print("Answer 2:", answer_2)  # 2399
