from collections import defaultdict
import itertools
from typing import Dict, Set

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

Point = complex

width = len(input_lines[0])
height = len(input_lines)
antennae_by_freq: Dict[str, Set[Point]] = defaultdict(set)
for r, line in enumerate(input_lines):
    for c, char in enumerate(line):
        if char != ".":
            antennae_by_freq[char].add(r * 1j + c)

have_antinodes: Set[Point] = set()
for freq, antennae in antennae_by_freq.items():
    for antenna_1, antenna_2 in itertools.combinations(antennae, 2):
        delta = antenna_2 - antenna_1
        antinode_1 = antenna_1 - delta
        antinode_2 = antenna_2 + delta
        for antinode in (antinode_1, antinode_2):
            if 0 <= antinode.real < width and 0 <= antinode.imag < height:
                have_antinodes.add(antinode)
answer_1 = len(have_antinodes)
print("Answer 1:", answer_1)  # 303

have_antinodes: Set[Point] = set()
for freq, antennae in antennae_by_freq.items():
    for antenna_1, antenna_2 in itertools.combinations(antennae, 2):
        delta = antenna_2 - antenna_1
        antinode = antenna_1
        while 0 <= antinode.real < width and 0 <= antinode.imag < height:
            have_antinodes.add(antinode)
            antinode += delta
        antinode = antenna_1
        delta = -delta
        while 0 <= antinode.real < width and 0 <= antinode.imag < height:
            have_antinodes.add(antinode)
            antinode += delta
answer_2 = len(have_antinodes)
print("Answer 2:", answer_2)  # 1045
