from yovirmac.modules.constants import *
import yovirmac.modules.lower_commands.read as read


def cell(num):
    value = memory[num]
    bits = []
    for i in range(capacity):
        bits.insert(0, str(value % 2))
        value >>= 1
    print("".join(bits), memory[num])


def number(num):
    print(memory[num])


def kind(num):
    print(types[memory[num]])


def none(num):
    value = read.none(num)
    if value == 0:
        print("none")


def link(num):
    value = read.link(num)
    print(f"link {value}")


def logic(num):
    value = read.logic(num)
    print("false" if not value else "true")


def string(num):
    print(read.string(num))
