with open("input.txt") as input_file:
    input_lines = input_file.readlines()
input_lines = [line.strip('\n') for line in input_lines]

data_line = [int(c) for c in input_lines[0]]
n = len(data_line)
checksum = 0
left_file_line_idx = 0
right_block_index_in_data_line = n - 2 if n % 2 == 0 else n - 1
right_block_id = n // 2 - 1 if n % 2 == 0 else n // 2
right_block_size_remaining = data_line[right_block_index_in_data_line]
for left_index_in_data_line, char in enumerate(data_line):
    i = left_index_in_data_line
    is_file_spot = i % 2 == 0
    left_block_id = i // 2
    number = int(char)
    if right_block_id == left_block_id:
        number = right_block_size_remaining
    if is_file_spot:
        for _ in range(number):
            checksum += left_file_line_idx * left_block_id
            left_file_line_idx += 1
    else:  # empty space, needs to be filled by the rightmost blocks' number
        for _ in range(number):
            checksum += left_file_line_idx * right_block_id
            left_file_line_idx += 1
            right_block_size_remaining -= 1
            if right_block_size_remaining == 0:
                right_block_id -= 1
                right_block_index_in_data_line -= 2
                right_block_size_remaining = data_line[right_block_index_in_data_line]
                if right_block_index_in_data_line < left_index_in_data_line:
                    break
    if right_block_index_in_data_line <= left_index_in_data_line:
        break

answer_1 = checksum
print("Answer 1:", answer_1)  # 6370402949053

# Part 2

checksum = 0
left_file_line_idx = 0
block_sizes_remaining = []  # technically I could optimize this from a list of ints to a list of bools, but meh
for i, char in enumerate(data_line):
    number = int(char)
    if i % 2 == 0:
        block_sizes_remaining.append(number)
right_block_index_in_data_line = n - 2 if n % 2 == 0 else n - 1
initial_right_block_id = n // 2 - 1 if n % 2 == 0 else n // 2
for left_index_in_data_line, char in enumerate(data_line):
    i = left_index_in_data_line
    is_file_spot = i % 2 == 0
    left_block_id = i // 2
    number = int(char)
    if is_file_spot and block_sizes_remaining[left_block_id] > 0:
        assert block_sizes_remaining[left_block_id] == number
        for _ in range(number):
            checksum += left_file_line_idx * left_block_id
            # print(left_block_id, end="")
            left_file_line_idx += 1
        block_sizes_remaining[left_block_id] = 0
    else:  # empty space, needs to be filled by the rightmost blocks' number
        # but only if it fits!  otherwise keep trying more to the left
        first_nonempty_line_idx = left_file_line_idx + number
        while left_file_line_idx < first_nonempty_line_idx:
            empties_remaining = first_nonempty_line_idx - left_file_line_idx
            for right_block_id in range(initial_right_block_id, -1, -1):
                if block_sizes_remaining[right_block_id] == 0:
                    continue
                if block_sizes_remaining[right_block_id] > empties_remaining:
                    continue
                for _ in range(block_sizes_remaining[right_block_id]):
                    checksum += left_file_line_idx * right_block_id
                    # print(right_block_id, end="")
                    left_file_line_idx += 1
                block_sizes_remaining[right_block_id] = 0
                break
            else:
                # print((first_nonempty_line_idx - left_file_line_idx) * ".", end="")
                left_file_line_idx = first_nonempty_line_idx
                break

answer_2 = checksum
print("Answer 2:", answer_2)  # 6398096697992
