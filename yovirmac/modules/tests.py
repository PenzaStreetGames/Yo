from yovirmac.main import *
from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.lower_commands import *
from yovirmac.modules.lower_commands import read as read
from yovirmac.modules.lower_commands import write as write
from yovirmac.modules.lower_commands import display as display
from yovirmac.modules.lower_commands import shift as shift
from yovirmac.modules.top_commands import *
from yovirmac.modules.tape_init import *
import random


def cell_overflow_write():
    """Проверка на переполнение путём записи больших значений"""
    value = 1
    for i in range(capacity + 4):
        write.cell(0, value)
        display.cell(0)
        value <<= 1
        value += 1


def cell_overflow_shift():
    """Проверка на переполнение путём битового сдига влево"""
    write.cell(0, 1)
    for i in range(capacity + 4):
        display.cell(0)
        shift.left(0, 1)
        write.bit(0, 0, 1)


def bit_writing():
    """Проверка на запись бита в ячейку"""
    write.clean(0)
    for i in range(capacity + 4):
        write.bit(0, i, 1)
        display.cell(0)
        write.bit(0, i, 0)


def number_writing():
    """Проверка на запись числа в ячейку"""
    write.clean(0)
    for i in range(20):
        number = random.randint(0, 2 ** 32 - 1)
        print(number)
        write.number(0, number)
        display.cell(0)


def type_writing():
    """Проверка на запись типа в ячеку"""
    for kind in types:
        write.kind(0, type)
        print(read.kind(0))
        display.cell(0)


def logic_writing():
    """Проверка на запись логических величин"""
    values = [0, 1, 2]
    for value in values:
        write.logic(0, value)
        print(value, read.logic(0))


def string_writing():
    """Проверка на запись введённой строки"""
    value = input()
    write.string(0, value)
    for i in range(len(value) + 1):
        print(read.cell(i), read.char(i))
    print(read.string(0))


def command_writing():
    """Проверка на запись команды"""
    for i in range(0, len(commands) + 1):
        try:
            write.command(0, i)
            display.command(0)
        except LowerCommandError as error:
            print(error)
    print()
    for abbrev in commands_abbreviation:
        write.command(0, abbrev)
        display.command(0)
    try:
        write.command(0, "no_command")
        display.command(0)
    except LowerCommandError as error:
        print(error)


def entity_writing():
    """Проверка на запись объектов"""
    entities = [
        [0, "none", None],
        [0, "link", 1000],
        [0, "command", 15],
        [0, "logic", 1],
        [0, "number", 255],
        [0, "string", "something"]
    ]
    for entity in entities:
        write.entity(*entity)
        display.cell(0)
        display.cell(1)
        display.entity(0)


def header_part_writing():
    """Проверка на запись части заголовка"""
    for header_type in seg_header.keys():
        write.header_part(0, header_type, {})
        display.header_part(0, header_type)
        for i in range(header_part_length):
            display.cell(i)
            write.clean(i)
        print()


def header_writing():
    """Проверка на запись заголовка"""
    for header_type in seg_header.keys():
        if header_type == "basic":
            continue
        write.header(0, header_type, {}, {})
        display.header(0)
        print()
