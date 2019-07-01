from yovirmac.modules.constants import *
import yovirmac.modules.lower_commands.read as read


def bit(num, digit):
    pass


def cell(num):
    value = memory[num]
    bits = []
    for i in range(capacity):
        bits.insert(0, str(value % 2))
        value >>= 1
    print("".join(bits), memory[num])


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


def string(num):
    print(read.string(num))


def entity(num):
    obj_type = read.kind(num)
    display_dictionary[obj_type](num + 1)


def system_area():
    pass


display_dictionary = {
    "none": none,
    "link": link,
    "command": command,
    "logic": logic,
    "number": number,
    "string": string
}