from yovirmac.modules.constants import *
from yovirmac.modules.types_control import memory_control
from yovirmac.modules.segment_control import change
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


def cells_stream(num, cells):
    for i in range(len(cells)):
        value = cells[i]
        cell(num + i, value)


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


def link_list(num, value):
    index = num
    for item in value:
        link(index, item)
        index += 1


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


def chars(num, value):
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


def char_list(num, value):
    index = num
    if type(value) == str:
        for symbol in value:
            char(index, symbol)
            index += 1
    elif type(value) == list:
        for item in value:
            number(index, item)
            index += 1


def array(num, args):
    i = -1
    for i in range(len(args)):
        value = args[i]
        entity(num + i * 2 + 1, "link", value)
    none(num + (i + 1) * 2 + 1, None)


def dictionary_item(num, args):
    args_num = len(args)
    if args_num != 3:
        raise LowerCommandError(f"Элемент словаря должен иметь 3 аргумента: "
                                f"ссылка на словарь, на ключ и на значение, "
                                f"а не {args_num}")
    for i in range(args_num):
        entity(num + i * 2 + 1, "link", args[i])


def entity(num, obj_type, value):
    kind(num, obj_type)
    if type(obj_type) == int:
        if value is None:
            value = default_values[types[obj_type]]
        write_list[obj_type](num + 1, value)
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


def header(num, base_args, special_args):
    segment_type = base_args["type"]
    header_part(num, "basic", base_args)
    header_part(num + header_base_part_length, seg_types[segment_type],
                special_args)


def segment(num, base_args, special_args):
    length = base_args.get("length", False)
    memory_control.add_cells(length)
    kind(num, types.index("segment"))
    header(num + 2, base_args, special_args)


def command_with_args(num, command_name, args):
    if len(args) != commands_args_number[command_name]:
        raise LowerCommandError(f"Неправильное число аргументов команды "
                                f"{command_name}: {len(args)} вместо "
                                f"{commands_args_number[command_name]}")
    entity(num, "command", command_name)
    index = num + 2
    for arg in args:
        obj_type = arg["type"]
        obj_value = arg["value"]
        entity(index, obj_type, obj_value)
        index += memory_control.determine_object_size(obj_type, obj_value)


write_list = [
    none,
    link,
    command,
    logic,
    number,
    chars,
    array,
    dictionary_item
]

write_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "chars": chars,
    "array": array,
    "dictionary_item": dictionary_item
}
