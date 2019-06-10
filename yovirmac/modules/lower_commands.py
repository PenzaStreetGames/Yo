from yovirmac.modules.constants import *


def get_full_cell():
    full_cell = 1
    for i in range(capacity):
        full_cell <<= 1
    full_cell -= 1
    return full_cell


full_cell = get_full_cell()


def read_cell(cell):  # read cell
    return memory[cell] & full_cell


def write_cell(cell, value):  # write cell
    memory[cell] = value & full_cell


def read_bit(cell, bit):  # read bit
    return (memory[cell] >> bit) & 1


def write_bit(cell, bit, value):  # write bit
    global memory
    shifted_bit = 1 << bit
    if value:
        memory[cell] |= shifted_bit
    else:
        inverse_bit = full_cell - shifted_bit
        memory[cell] &= inverse_bit


def add_cells(number):
    global memory
    memory += [0] * number


def left_shift(cell, shift):
    global memory
    memory[cell] <<= shift
    memory[cell] &= full_cell


def right_shift(cell, shift):
    global memory
    memory[cell] >>= shift



def print_cell(cell):
    value = memory[cell]
    bits = []
    for i in range(capacity):
        bits.insert(0, str(value % 2))
        value >>= 1
    print("".join(bits), memory[cell])
