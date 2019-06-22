from yovirmac.modules.constants import *


def get_full_cell():
    raw_full_cell = 1
    for i in range(capacity):
        raw_full_cell <<= 1
    raw_full_cell -= 1
    return raw_full_cell


full_cell = get_full_cell()


def read_cell(cell):
    return memory[cell] & full_cell


def write_cell(cell, value):
    memory[cell] = value & full_cell


def clean_cell(cell):
    memory[cell] = 0


def read_bit(cell, bit):
    return (memory[cell] >> bit) & 1


def write_bit(cell, bit, value):
    shifted_bit = 1 << bit
    if value:
        memory[cell] |= shifted_bit
        memory[cell] &= full_cell
    else:
        inverse_bit = full_cell - shifted_bit
        memory[cell] &= inverse_bit


def add_cells(number):
    global memory
    memory += [0] * number


def bit_left_shift(cell, shift):
    global memory
    memory[cell] <<= shift
    memory[cell] &= full_cell


def bit_right_shift(cell, shift):
    global memory
    memory[cell] >>= shift


def print_cell(cell):
    value = memory[cell]
    bits = []
    for i in range(capacity):
        bits.insert(0, str(value % 2))
        value >>= 1
    print("".join(bits), memory[cell])


def write_number(cell, number):
    memory[cell] = number


def read_number(cell):
    return memory[cell]


def print_number(cell):
    print(memory[cell])


def write_type(cell, value):
    if type(value) == int:
        write_cell(cell, value)
    elif type(value) == str:
        write_cell(cell, types.index(value))


def read_type(cell):
    return types[memory[cell]]


def print_type(cell):
    print(types[memory[cell]])


def write_none(cell):
    memory[cell] = 0


def read_none(cell):
    return memory[cell]


def print_none(cell):
    value = read_none(cell)
    if value == 0:
        print("none")


def write_link(cell, value):
    memory[cell] = value


def read_link(cell):
    return memory[cell]


def print_link(cell):
    value = read_link(cell)
    print(f"link {value}")


def write_logic(cell, value):
    memory[cell] = 0 if not value else 1


def read_logic(cell):
    return memory[cell]


def print_logic(cell):
    value = read_logic(cell)
    print("false" if not value else "true")


def write_char(cell, value):
    memory[cell] = ord(value)


def read_char(cell):
    return chr(memory[cell])


def write_string(cell, value):
    index = cell
    if type(value) == str:
        for symbol in value:
            write_char(index, symbol)
            index += 1
        write_none(index)
    elif type(value) == list:
        for number in value:
            write_number(index, number)
            index += 1
        write_none(index)


def read_string(cell, output="str"):
    index = cell
    symbol = read_number(cell)
    if output == "str":
        result = ""
        while symbol != 0:
            result += chr(symbol)
            index += 1
            symbol = read_number(index)
        return result
    elif output == "list":
        result = []
        while symbol != 0:
            result.append(symbol)
            index += 1
            symbol = read_number(index)
        return result


def print_string(cell):
    print(read_string(cell))


def write_segment(cell, type):
    pass


def write_segment_header(cell):
    pass


def write_segment_base_header(cell):
    pass


def write_segment_special_header(cell):
    pass
