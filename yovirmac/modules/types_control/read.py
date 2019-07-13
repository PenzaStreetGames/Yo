from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import memory_control


def bit(num, digit):
    return (memory[num] >> digit) & 1


def sign(num):
    return bit(num, 31)


def cell(num):
    return memory[num] & full_cell


def signed_cell(num):
    cell_sign = sign(num)
    value = cell(num)
    if cell_sign == 1:
        value -= full_cell + 1
    return value


def kind(num):
    return types[memory[num]]


def none(num):
    return memory[num]


def link(num):
    return memory[num]


def link_list(num, end):
    result = []
    for i in range(num, end):
        result += [link(i)]
    return result


def command(num):
    return memory[num]


def logic(num):
    return bool(memory[num])


def number(num):
    return signed_cell(num)


def char(num):
    return chr(memory[num])


def chars(num, output="str"):
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


def char_list(num, end, output="str"):
    if output == "str":
        result = ""
        for i in range(num, end):
            result += char(i)
        return result
    elif output == "list":
        result = []
        for i in range(num, end):
            result += number(i)
        return result


def array(num):
    args = []
    index = num + 1
    obj_type, value = entity(index)
    while obj_type != "none":
        args += [value]
        index += 2
        obj_type, value = entity(index)
    return args


def dictionary_item(num):
    result = []
    for i in range(3):
        arg_type, arg = entity(num + i * 2 + 1)
        if arg_type != "link":
            LowerCommandError(f"Аргумент элемента словаря имеет тип {arg_type},"
                              f" а не link")
        result += [arg]
    return result


def entity(num):
    obj_type = kind(num)
    if obj_type not in read_dictionary:
        raise LowerCommandError(f"Неподдерживаемый тип для чтения {obj_type}")
    value = read_dictionary[obj_type](num + 1)
    return obj_type, value


def header_part(num, header_type):
    args = {}
    for i in range(len(seg_header[header_type])):
        attribute_name = seg_header[header_type][i]
        attribute = entity(num + i * 2)[1]
        args[attribute_name] = attribute
    return args


def header(num):
    base_args = header_part(num, "basic")
    args = header_part(num + header_base_part_length,
                       seg_types[base_args["type"]])
    return base_args, args


def segment(num):
    args, base_args = header(num + 2)
    return args, base_args


def command_with_args(num):
    args = []
    obj_type, command_name = entity(num)
    index = num + 2
    for i in range(commands_args_number[commands_abbreviation[command_name]]):
        obj_type, value = entity(index)
        args += [{"type": obj_type, "value": value}]
        index += memory_control.determine_object_size(obj_type, value)
    return command_name, args


read_list = [
    none,
    link,
    command,
    logic,
    number,
    chars,
    array,
    dictionary_item
]

read_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "chars": chars,
    "array": array,
    "dictionary_item": dictionary_item
}
