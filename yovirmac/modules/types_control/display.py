from yovirmac.modules.constants import *
from yovirmac.modules.types_control import read, memory_control


def bit(num, digit):
    pass


def cell(num):
    value = memory[num]
    bits = []
    for i in range(capacity):
        bits.insert(0, str(value % 2))
        value >>= 1
    print("".join(bits), memory[num])


def signed_cell(num):
    value = memory[num]
    bits = []
    for i in range(capacity):
        bits.insert(0, str(value % 2))
        value >>= 1
    neg_value = read.signed_cell(num)
    print("".join(bits), neg_value)


def kind(num):
    print(types[memory[num]])


def none(num):
    value = read.none(num)
    if value == 0:
        print("none")


def link(num):
    value = read.link(num)
    print(f"link {value}")


def command(num):
    result = read.command(num)
    print(f"{result} {commands[result]}")


def logic(num):
    value = read.logic(num)
    print("false" if not value else "true")


def number(num):
    print(memory[num])


def char(num):
    print(f"char \"{read.char(num)}\"")


def chars(num):
    print(f"\"{read.chars(num)}\"")


def array(num):
    print("array:", *read.array(num))


def dictionary_item(num):
    print(read.dictionary_item(num))


def entity(num):
    obj_type = read.kind(num)
    display_dictionary[obj_type](num + 1)


def header_part(num, header_type):
    args = read.header_part(num, header_type)
    for arg_name in seg_header[header_type]:
        print(f"{arg_name}: {args[arg_name]}")


def header(num):
    base_args, args = read.header(num)
    header_type = base_args["type"]
    for arg_name in seg_header["basic"]:
        print(f"{arg_name}: {base_args[arg_name]}")
    print()
    for arg_name in seg_header[seg_types[header_type]]:
        print(f"{arg_name}: {args[arg_name]}")


def segment(num):
    header(num + 2)


def command_with_args(num):
    print(num, end=" ")
    entity(num)
    args = []
    obj_type, command_name = read.entity(num)
    index = num + 2
    for i in range(commands_args_number[commands_abbreviation[command_name]]):
        obj_type, value = read.entity(index)
        print("\t", end="")
        entity(index)
        index += memory_control.determine_object_size(obj_type, value)


display_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "chars": chars,
    "array": array,
    "dictionary_item": dictionary_item
}
