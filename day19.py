import re
from collections import defaultdict
from functools import lru_cache
from typing import Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

all_available_towels = tuple(input_lines[0].split(", "))


# @lru_cache
# def try_solving(target_pattern: str, from_towel_idx: int) -> bool:
#     if target_pattern == "":
#         return True
#     if from_towel_idx >= len(all_available_towels):
#         return False
# optimize, fail early if there's an impossible letter (substring of length 1)
# for letter in "wubrg":
#     if letter in target_pattern:
#         if not any(letter in towel for towel in towels):
#             return False
# towels = tuple(tow for tow in towels if tow in target_pattern)
# for i, towel in enumerate(towels):
#     if target_pattern.startswith(towel):
#         remaining_pattern = target_pattern[len(towel):]
#         towels_without_this_one = towels[:i] + towels[i + 1:]
#         if (try_solving(towels, remaining_pattern) or
#                 try_solving(towels_without_this_one, target_pattern)):
#             return True

# towel = towels[0]
# idx = target_pattern.find(towel)
# if idx == -1:
#     return try_solving(towels[1:], target_pattern)
# if try_solving(towels, target_pattern[idx + 1:]):
#     if try_solving(towels, target_pattern[:idx]):
#         return True
# if try_solving(towels[1:], target_pattern):
#     return True


# towel = all_available_towels[from_towel_idx]
# idx = target_pattern.find(towel)
# if idx == -1:
#     return try_solving(target_pattern, from_towel_idx + 1)
# if try_solving(target_pattern[idx + 1:], from_towel_idx):
#     if try_solving(target_pattern[:idx], from_towel_idx):
#         return True
# if try_solving(target_pattern, from_towel_idx + 1):
#     return True

# return False


class TrieNode:
    def __init__(self, prefix: str):
        self.children = {}
        self.is_end_of_word = False
        self.prefix = prefix

    def add_word(self, word: str):
        current_node = self
        for letter in word:
            if letter not in current_node.children:
                current_node.children[letter] = TrieNode(current_node.prefix + letter)
            current_node = current_node.children[letter]
        current_node.is_end_of_word = True

    def __repr__(self):
        return f"TrieNode({self.prefix}{'.' if self.is_end_of_word else '-'})"


trie_root = TrieNode("")
for towel in all_available_towels:
    trie_root.add_word(towel)


def match_with_trie(target_pattern: str):
    idx = 0
    nodes = {trie_root: 1}
    while idx < len(target_pattern):
        letter = target_pattern[idx]
        next_nodes = {}
        while nodes:
            node, count = nodes.popitem()
            if node.is_end_of_word and letter in trie_root.children:
                next_nodes[trie_root.children[letter]] = next_nodes.get(trie_root.children[letter], 0) + count
            if letter in node.children:
                next_nodes[node.children[letter]] = next_nodes.get(node.children[letter], 0) + count
        if not next_nodes:
            return False
        nodes = next_nodes
        idx += 1
    return sum(count if node.is_end_of_word else 0 for node, count in nodes.items())


answer_1 = 0
answer_2 = 0
# towels_regex = re.compile("(" + "|".join(all_available_towels) + ")*")
for pattern in input_lines[2:]:
    # print(pattern)
    # if try_solving(all_available_towels, pattern):
    # if try_solving(pattern, 0):
    # if towels_regex.fullmatch(pattern):
    count = match_with_trie(pattern)
    answer_1 += 1 if count > 0 else 0
    answer_2 += count

print("Answer 1:", answer_1)  # 251
print("Answer 2:", answer_2)  #
