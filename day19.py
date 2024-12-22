with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

all_available_towels = tuple(input_lines[0].split(", "))


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

    def add_word(self, word: str):
        current_node = self
        for letter in word:
            if letter not in current_node.children:
                current_node.children[letter] = TrieNode()
            current_node = current_node.children[letter]
        current_node.is_end_of_word = True


trie_root = TrieNode()
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
for pattern in input_lines[2:]:
    count = match_with_trie(pattern)
    answer_1 += 1 if count > 0 else 0
    answer_2 += count

print("Answer 1:", answer_1)  # 251
print("Answer 2:", answer_2)  # 616957151871345
