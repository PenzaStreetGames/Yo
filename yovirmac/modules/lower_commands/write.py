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


def none(num, value):
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
        none(index, None)
    elif type(value) == list:
        for item in value:
            number(index, item)
            index += 1
        none(index, None)


def entity(num, obj_type, value):
    kind(num, obj_type)
    if type(obj_type) == int:
        if value is None:
            value = default_values[types[obj_type]]
        write_list[obj_type](num, value)
    elif type(obj_type) == str:
        if value is None:
            value = default_values[obj_type]
        write_dictionary[obj_type](num + 1, value)


def header_part(num, header_type, args):
    for i in range(len(seg_header[header_type])):
        attribute = seg_header[header_type][i]
        attribute_type = seg_header_types[header_type][attribute]
        if not args.get(attribute, False):
            entity(num + i * 2, attribute_type, None)
        else:
            entity(num + i * 2, attribute_type, args[attribute])


def system_area():
    args = {
        "type": seg_types.index("system"),
        "length": 64,
        "segment_end": 64
    }
    header_part(0, "basic", args)


write_list = [
    none,
    link,
    command,
    logic,
    number,
    string
]

write_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "string": string
}
