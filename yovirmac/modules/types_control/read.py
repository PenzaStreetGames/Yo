from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import memory_control


def bit(num, digit):
    return (memory[num] >> digit) & 1


def cell(num):
    return memory[num] & full_cell


def kind(num):
    return types[memory[num]]


def none(num):
    return memory[num]


def link(num):
    return memory[num]


def command(num):
    return memory[num]


def logic(num):
    return memory[num]


def number(num):
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


def string_part(num, stop, past_data=None, begin=True):
    index = num
    symbol = number(index)
    result = ""
    while symbol != 0 and index < stop:
        result += chr(symbol)
        index += 1
        symbol = number(index)
    end = True
    if index == stop:
        end = False
    elif symbol == 0:
        end = True
    return result, end


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


def dictionary_item_part(num, stop, past_data=None, begin=True):
    result = []
    place = stop - num + 1
    if begin:
        for i in range(3):
            if place >= 3 + i * 2:
                arg_type, arg = entity(num + i * 2 + 1)
                if arg_type != "link":
                    LowerCommandError(f"Аргумент элемента словаря имеет тип "
                                      f"{arg_type}, а не link")
                result += [arg]
        if len(result) != 3:
            end = False
        else:
            end = True
    else:
        for i in range(3 - len(past_data)):
            if place >= 2 + i * 2:
                arg_type, arg = entity(num + i * 2)
                if arg_type != "link":
                    LowerCommandError(f"Аргумент элемента словаря имеет тип "
                                      f"{arg_type}, а не link")
                result += [arg]
        if len(past_data) + len(result) != 3:
            end = False
        else:
            end = True
    return result, end


def entity(num):
    obj_type = kind(num)
    if obj_type not in read_dictionary:
        raise LowerCommandError(f"Неподдерживаемый тип для чтения {obj_type}")
    value = read_dictionary[obj_type](num + 1)
    return obj_type, value


def entity_part(num, obj_type=None, past_data=None, stop=None, begin=True):
    if begin:
        obj_type = kind(num)
        if obj_type in read_part_dictionary:
            value, end = read_part_dictionary[obj_type](
                num + 1, stop, past_data=past_data, begin=begin)
        else:
            value, end = read_dictionary[obj_type](num + 1), True
    else:
        if obj_type in read_part_dictionary:
            value, end = read_part_dictionary[obj_type](
                num, stop, past_data=past_data, begin=begin)
        else:
            raise LowerCommandError(f"Тип {obj_type} не поддерживает "
                                    f"межсегментное чтение")
    return obj_type, value, end


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
    string,
    array,
    dictionary_item
]

read_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "string": string,
    "array": array,
    "dictionary_item": dictionary_item
}

read_part_dictionary = {
    "string": string_part,
    "dictionary_item": dictionary_item_part
}
