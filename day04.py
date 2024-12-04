with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

LETTER_HASHES = {
    "X": 1,
    "M": 2,
    "A": 4,
    "S": 8,
}
HASH_OF_XMAS = LETTER_HASHES["X"] * 16 * 16 * 16 + LETTER_HASHES["M"] * 16 * 16 + LETTER_HASHES["A"] * 16 + LETTER_HASHES["S"]

matrix = input_lines
N = len(matrix)
answer_1 = 0
def count_xmas_in_iterated_string(some_list) -> int:
    some_list = list(some_list)
    counter = 0
    if len(some_list) < 4:
        return 0
    iterator = iter(some_list)
    sliding_window_hash = \
        LETTER_HASHES[next(iterator)] * 16 * 16 + \
        LETTER_HASHES[next(iterator)] * 16 + \
        LETTER_HASHES[next(iterator)]
    for char in iterator:
        sliding_window_hash *= 16
        sliding_window_hash += LETTER_HASHES[char]
        if sliding_window_hash == HASH_OF_XMAS:
            counter += 1
        sliding_window_hash = sliding_window_hash % (16 ** 3)
    return counter

for i in range(N):
    # rows
    answer_1 += count_xmas_in_iterated_string(list(matrix[i]))
    # rows backwards
    answer_1 += count_xmas_in_iterated_string(reversed(matrix[i]))
for j in range(N):
    # columns
    answer_1 += count_xmas_in_iterated_string(list(row[j] for row in matrix))
    # columns backwards
    answer_1 += count_xmas_in_iterated_string(reversed(list(row[j] for row in matrix)))

# now diagonals
for j in range(N):
    # starting in row 0, continuing down-and-right
    answer_1 += count_xmas_in_iterated_string(matrix[k][j + k] for k in range(N - j))
    # also reversed
    answer_1 += count_xmas_in_iterated_string(reversed(list(matrix[k][j + k] for k in range(N - j))))
    # starting in row 0, continuing down-and-left
    answer_1 += count_xmas_in_iterated_string(matrix[k][j - k] for k in range(j + 1))
    # also reversed
    answer_1 += count_xmas_in_iterated_string(reversed(list(matrix[k][j - k] for k in range(j + 1))))
    if j != 0 and j != N - 1: # (avoid double-counting main diagonals)
        # starting in row N-1, continuing up-and-right
        answer_1 += count_xmas_in_iterated_string(matrix[N - 1 - k][j + k] for k in range(N - j))
        # also reversed
        answer_1 += count_xmas_in_iterated_string(reversed(list(matrix[N - 1 - k][j + k] for k in range(N - j))))
        # starting in row N-1, continuing up-and-left
        answer_1 += count_xmas_in_iterated_string(matrix[N - 1 - k][j - k] for k in range(j + 1))
        # also reversed
        answer_1 += count_xmas_in_iterated_string(reversed(list(matrix[N - 1 - k][j - k] for k in range(j + 1))))






print("Answer 1:", answer_1) # 2567



answer_2 = 0

for i in range(1, N - 1):
    for j in range(1, N - 1):
        # check for:
        # M.S
        # .A.
        # M.S
        # or e.g.
        # M.M
        # .A.
        # S.S
        # (four variations)
        diag_1 = [matrix[i - 1][j - 1], matrix[i][j], matrix[i + 1][j + 1]]
        diag_2 = [matrix[i - 1][j + 1], matrix[i][j], matrix[i + 1][j - 1]]
        d1 = "".join(diag_1)
        d2 = "".join(diag_2)
        d3 = d1[::-1]
        d4 = d2[::-1]
        mas_count = 0
        for d in [d1, d2, d3, d4]:
            if d == "MAS":
                mas_count += 1
        if mas_count >= 2:  # micro optimization
            answer_2 += 1



print("Answer 2:", answer_2)  # 2029
