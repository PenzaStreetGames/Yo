from yovirmac.modules.constants import *


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


def entity(num):
    obj_type = kind(num)
    value = read_dictionary[obj_type](num + 1)
    return obj_type, value


def header_part(num, header_type):
    args = {}
    for i in range(len(seg_header[header_type])):
        attribute_name = seg_header[header_type][i]
        attribute = entity(num + i * 2)[1]
        args[attribute_name] = attribute
    return args


read_list = [
    none,
    link,
    command,
    logic,
    number,
    string
]

read_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "string": string
}
