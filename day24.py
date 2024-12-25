import re
from typing import Dict, Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

initial_values: Dict[str, int] = {}
equations: Dict[str, Tuple[str, str, str]] = {}  # c: (a, OP, b)
for line in input_lines:
    if ":" in line:
        wire_s, value_s = line.split(": ")
        initial_values[wire_s] = int(value_s)
    elif "->" in line:
        a, op, b, c = re.match(r"(.+?) (.+?) (.+?) -> (.+)", line).groups()
        op = "XOR" if op == "OR" else op
        equations[c] = (a, op, b)

answer_1 = 0
calculated_values = {}


def lazy_get_or_calc(wire: str):
    if wire not in calculated_values:
        if wire in initial_values:
            calculated_values[wire] = initial_values[wire]
        else:
            left, operation, right = equations[wire]
            if operation == "AND":
                calculated_values[wire] = lazy_get_or_calc(left) & lazy_get_or_calc(right)
            elif operation == "XOR":
                calculated_values[wire] = lazy_get_or_calc(left) ^ lazy_get_or_calc(right)
            elif operation == "OR":
                # ohoho, XOR = OR in this context!  because of how this "two number addition" was designed
                # calculated_values[wire] = lazy_get_or_calc(left) ^ lazy_get_or_calc(right)
                # calculated_values[wire] = lazy_get_or_calc(left) | lazy_get_or_calc(right)
                raise ValueError("unexpected OR")
    return calculated_values[wire]


for i in range(100):
    z_wire_i = f"z" + str(i).rjust(2, "0")
    if z_wire_i not in equations:
        break
    answer_1 += 2 ** i * lazy_get_or_calc(z_wire_i)
print("Answer 1:", answer_1)  # 41324968993486





compare_triplet = lambda trip1, trip2: trip1 == trip2 or trip1 == trip2[::-1]


def find_by_eq(l, o, r):
    return next(w for w in equations if compare_triplet(equations[w], (l, o, r)))


MANUAL_SWAPS_FOUND = [
    ('z08', ('mcr', 'AND', 'sjd'), 'SHOULD BE', ('mcr', 'XOR', 'sjd')),
    ('rds', ('x14', 'XOR', 'y14'), 'SHOULD BE', ('x14', 'XOR', 'y14')),
    ('z18', ('x18', 'AND', 'y18'), 'SHOULD BE', ('mfk', 'XOR', 'fmm')),
    ('z23', ('fwj', 'XOR', 'vsq'), 'SHOULD BE', ('qmd', 'XOR', 'bpr')),
]
swaps_made = []
print()
for msf in MANUAL_SWAPS_FOUND:
    wire, curr_eq, _should_be, new_eq = msf
    swap_target = find_by_eq(*new_eq)
    equations[wire], equations[swap_target] = equations[swap_target], equations[wire]
    swaps_made.append((wire, swap_target))
    print(f"Swapped {wire} with {swap_target}")
print()


def calc_set_role(name, left, op, right):
    try:
        roles[name] = find_by_eq(roles[left], op, roles[right])
    except StopIteration:
        print(f"Could not find [{roles[left]} {op} {roles[right]}], was trying to set {name}")
        print(f"               [{left} {op} {right}]")
        raise


roles = {}
for i in range(100):
    roles[f"a-x-{i:02}"] = f"x{i:02}"
    roles[f"a-y-{i:02}"] = f"y{i:02}"
calc_set_role("b-xor-00", "a-x-00", "XOR", "a-y-00")  # = z00
calc_set_role("b-and-00", "a-x-00", "AND", "a-y-00")
calc_set_role("b-xor-01", "a-x-01", "XOR", "a-y-01")
calc_set_role("b-and-01", "a-x-01", "AND", "a-y-01")
calc_set_role("c-xor-a00x01", "b-xor-01", "XOR", "b-and-00")  # = z01
calc_set_role("c-and-a00x01", "b-xor-01", "AND", "b-and-00")
calc_set_role("d-xor-a01aa00x01", "b-and-01", "XOR", "c-and-a00x01")
# pattern marker...
calc_set_role("b-xor-02", "a-x-02", "XOR", "a-y-02")
calc_set_role("b-and-02", "a-x-02", "AND", "a-y-02")
calc_set_role("c-xor-a01x02", "b-xor-02", "XOR", "d-xor-a01aa00x01")  # = z02
calc_set_role("c-and-a01x02", "b-xor-02", "AND", "d-xor-a01aa00x01")
calc_set_role("d-xor-a02aa01x02", "b-and-02", "XOR", "c-and-a01x02")
# from here on, the pattern repeats, incrementing all numbers by 1)

for i in range(3, 45):
    try:
        m2 = f"{i - 2:02}"
        m1 = f"{i - 1:02}"
        nn = f"{i:02}"
        calc_set_role(f"b-xor-{nn}", f"a-x-{nn}", "XOR", f"a-y-{nn}")
        calc_set_role(f"b-and-{nn}", f"a-x-{nn}", "AND", f"a-y-{nn}")
        calc_set_role(f"c-xor-a{m1}x{nn}", f"b-xor-{nn}", "XOR", f"d-xor-a{m1}aa{m2}x{m1}")
        calc_set_role(f"c-and-a{m1}x{nn}", f"b-xor-{nn}", "AND", f"d-xor-a{m1}aa{m2}x{m1}")
        calc_set_role(f"d-xor-a{nn}aa{m1}x{nn}", f"b-and-{nn}", "XOR", f"c-and-a{m1}x{nn}")
        assert f'z{nn}' == roles[f"c-xor-a{m1}x{nn}"]
    except (StopIteration, AssertionError):
        print()
        print(f"Stopped at i={i}, something was sabotaged here.")
        print()
        for role, wire in list(roles.items())[-13:]:
            if wire in equations:
                print(wire, "    ", equations[wire], "    ", role)
        break
assert f'z44' == roles[f"c-xor-a43x44"]
assert f'z45' == roles[f"d-xor-a44aa43x44"]  # special case, because it's the last one -- there's no x45 or y45

# flatten swap list
all_wires_swapped = sorted([w for pair in swaps_made for w in pair])
print("Answer 2:", ",".join(all_wires_swapped))  # bmn,jss,mvb,rds,wss,z08,z18,z23
