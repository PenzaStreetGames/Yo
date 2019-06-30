from yovirmac.modules.constants import *
from yovirmac.modules.lower_commands import read
from yovirmac.modules.errors import *


def bit(num, digit, value):
    shifted_bit = 1 << digit
    if value:
        memory[num] |= shifted_bit
        memory[num] &= full_cell
    else:
        inverse_bit = full_cell - shifted_bit
        memory[num] &= inverse_bit


def cell(num, value):
    memory[num] = value & full_cell


def clean(num):
    memory[num] = 0


def kind(num, value):
    if type(value) == int:
        if not(0 <= value < len(types)):
            raise LowerCommandError(f"Неподдерживаемый индекс типа: {value}")
        cell(num, value)
    elif type(value) == str:
        if value not in types:
            raise LowerCommandError(f"Неизвестный тип: {value}")
        cell(num, types.index(value))


def none(num):
    memory[num] = 0


def link(num, value):
    memory[num] = value


def command(num, value):
    if type(value) == int:
        if not(0 <= value < len(commands)):
            raise LowerCommandError(f"Неподдерживаемый номер команды: {value}")
        memory[num] = value
    elif type(value) == str:
        if value not in commands_abbreviation:
            raise LowerCommandError(f"Неизвестная команда: {value}")
        memory[num] = commands_abbreviation.index(value)


def logic(num, value):
    memory[num] = 0 if not value else 1


def number(num, value):
    memory[num] = value


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
        for item in value:
            number(index, item)
            index += 1
        none(index)


def entity(num, obj_type, value):
    pass


def base_header():
    pass


def system_area():
    base_args = {
        "type": seg_types.index("system"),
        "length": 64,
        "segment_end": 64
    }
    base_header()
