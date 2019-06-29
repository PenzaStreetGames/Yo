from yovirmac.modules.constants import *
from yovirmac.modules.lower_commands import read


def cell(num, value):
    memory[num] = value & full_cell


def bit(num, bit, value):
    shifted_bit = 1 << bit
    if value:
        memory[num] |= shifted_bit
        memory[num] &= full_cell
    else:
        inverse_bit = full_cell - shifted_bit
        memory[num] &= inverse_bit


def number(num, number):
    memory[num] = number


def kind(num, value):
    if type(value) == int:
        cell(num, value)
    elif type(value) == str:
        cell(num, types.index(value))


def none(num):
    memory[num] = 0


def link(num, value):
    memory[num] = value


def logic(num, value):
    memory[num] = 0 if not value else 1


def char(num, value):
    memory[num] = ord(value)


def string(num, value):
    index = num
    if type(value) == str:
        for symbol in value:
            char(index, symbol)
            index += 1
        none(index)
    elif type(value) == list:
        for number in value:
            number(index, number)
            index += 1
        none(index)
