from yovirmac.modules.constants import *


def left(num, shift):
    global memory
    memory[num] <<= shift
    memory[num] &= full_cell


def right(num, shift):
    global memory
    memory[num] >>= shift
