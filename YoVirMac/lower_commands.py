from ..constants import *


def get_full_cell():
    full_cell = 1
    for i in range(capacity):
        full_cell <<= 1
    full_cell -= 1
    return full_cell


full_cell = get_full_cell()

# низшие машинные команды
def rdc(memory, cell):  # read cell
    return memory[cell] & full_cell


def wrc(memory, cell, value):  # write cell
    memory[cell] = value & full_cell


def rdb(cell, bit):  # read bit
    return (memory[cell] >> bit) & 1


def wrb(cell, bit, value):  # write bit
    global memory
    shifted_bit = 1 << bit
    if value:
        memory[cell] |= shifted_bit
    else:
        inverse_bit = full_cell - shifted_bit
        memory[cell] &= inverse_bit
