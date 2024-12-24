import itertools
from typing import Dict, Tuple, Set, List

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

edges = set()
nodes = set()
for line in input_lines:
    node1, node2 = line.split("-")
    nodes.add(node1)
    nodes.add(node2)
    edges.add((node1, node2))
    edges.add((node2, node1))

known_triangles = set()
for node in nodes:
    if node.startswith("t"):
        for node2 in nodes:
            if (node, node2) in edges:
                for node3 in nodes:
                    if (node, node2) in edges and (node2, node3) in edges and (node3, node) in edges:
                        # found triangle that starts with t
                        triangle_in_order = tuple(sorted([node, node2, node3]))
                        known_triangles.add(triangle_in_order)
answer_1 = len(known_triangles)
print("Answer 1:", answer_1)  # 1151

# for part 2 we need to find the largest "clique" in the graph
# we can use the Bron-Kerbosch algorithm for this (says the AI)
# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
# but I want to solve it myself first, using... my brain
#
# for size in range(len(nodes), 0, -1):
#     print("Trying size:", size)
#     found_giant_clique = None
#     for comb in itertools.combinations(nodes, size):
#         if all((node1, node2) in edges for node1, node2 in itertools.combinations(comb, 2)):
#             found_giant_clique = comb
#             break
#     if found_giant_clique:
#         print("Answer 2:", ",".join(sorted(found_giant_clique)))
#         break


# algorithm BronKerbosch2(R, P, X) is
#     if P and X are both empty then
#         report R as a maximal clique
#     choose a pivot vertex u in P ⋃ X
#     for each vertex v in P \ N(u) do
#         BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#         P := P \ {v}
#         X := X ⋃ {v}

neighbors = {
    node: {n for n in nodes if (n, node) in edges}
    for node in nodes}

def bronkerb1(r: Set[str], p: Set[str], x: Set[str], found_so_far: List[Set[str]]):
    if not p and not x:
        found_so_far.append(r)
    for v in p.copy():
        neighbors_of_v = neighbors[v]
        set_only_v = {v}
        bronkerb1(
            r.union(set_only_v),
            p.intersection(neighbors_of_v),
            x.intersection(neighbors_of_v),
            found_so_far
        )
        p.remove(v)
        x.add(v)
    return None

maybe_cliques = []
bronkerb1(set(), nodes, set(), maybe_cliques)
biggest_clique_set = max(maybe_cliques, key=len)
answer_2 = ",".join(sorted(biggest_clique_set))
print("Answer 2:", answer_2)  # ar,cd,hl,iw,jm,ku,qo,rz,vo,xe,xm,xv,ys