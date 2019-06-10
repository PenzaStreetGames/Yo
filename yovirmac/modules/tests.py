from yovirmac.main import *
from yovirmac.modules.constants import *
from yovirmac.modules.lower_commands import *
from yovirmac.modules.top_commands import *
from yovirmac.modules.tape_init import *
import random


def cell_overflow_write():
    """Проверка на переполнение путём записи больших значений"""
    add_cells(1)
    value = 1
    for i in range(capacity + 4):
        write_cell(0, value)
        print_cell(0)
        value <<= 1
        value += 1


def cell_overflow_shift():
    """Проверка на переполнение путём битового сдига влево"""
    write_cell(0, 1)
    for i in range(capacity + 4):
        print_cell(0)
        bit_left_shift(0, 1)
        write_bit(0, 0, 1)


def bit_writing():
    """Проверка на запись бита в ячейку"""
    clean_cell(0)
    for i in range(capacity + 4):
        write_bit(0, i, 1)
        print_cell(0)
        write_bit(0, i, 0)


def number_writing():
    """Проверка на запись числа в ячейку"""
    clean_cell(0)
    for i in range(20):
        number = random.randint(0, 2 ** 32 - 1)
        print(number)
        write_number(0, number)
        print_cell(0)


def type_writing():
    """Проверка на запись типа в ячеку"""
    for type in types:
        write_type(0, type)
        print(read_type(0))
        print_cell(0)
