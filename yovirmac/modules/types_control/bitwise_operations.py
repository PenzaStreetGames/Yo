from yovirmac.modules.constants import *


def bitwise_not(num):
    global memory
    memory[num] = ~memory[num] & full_cell


def bitwise_and(num, mask):
    global memory
    memory[num] = memory[num] & mask


def bitwise_or(num, mask):
    global memory
    memory[num] = memory[num] | mask


def bitwise_xor(num, mask):
    global memory
    memory[num] = memory[num] ^ mask
