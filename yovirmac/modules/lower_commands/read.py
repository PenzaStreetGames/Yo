from yovirmac.modules.constants import *


def cell(num):
    return memory[num] & full_cell


def bit(num, bit):
    return (memory[num] >> bit) & 1


def number(num):
    return memory[num]


def kind(num):
    return types[memory[num]]


def none(num):
    return memory[num]


def link(num):
    return memory[num]


def logic(num):
    return memory[num]


def char(num):
    return chr(memory[num])


def string(num, output="str"):
    index = num
    symbol = number(num)
    if output == "str":
        result = ""
        while symbol != 0:
            result += chr(symbol)
            index += 1
            symbol = number(index)
        return result
    elif output == "list":
        result = []
        while symbol != 0:
            result.append(symbol)
            index += 1
            symbol = number(index)
        return result


def write_command(num, value):
    pass
