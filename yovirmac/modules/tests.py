from yovirmac.main import *
from yovirmac.modules.constants import *
from yovirmac.modules.lower_commands import *
from yovirmac.modules.top_commands import *
from yovirmac.modules.tape_init import *


def cell_overflow_write():
    add_cells(1)
    value = 1
    for i in range(capacity + 4):
        write_cell(0, value)
        print_cell(0)
        value <<= 1
        value += 1


def cell_overflow_shift():
    write_cell(0, 1)
    for i in range(capacity + 4):
        print_cell(0)
        left_shift(0, 1)
        write_bit(0, 0, 1)
