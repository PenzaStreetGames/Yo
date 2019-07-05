from yovirmac.modules.tests import *
from yovirmac.modules.types_control import memory_control

tests = {
    1: cell_overflow_write,
    2: cell_overflow_shift,
    3: bit_writing,
    4: number_writing,
    5: type_writing,
    6: logic_writing,
    7: string_writing,
    8: command_writing,
    9: entity_writing,
    10: header_part_writing,
    11: header_writing,
    12: attribute_writing
}

memory_control.add_cells(64)
while True:
    number = int(input())
    print(tests[number].__doc__)
    tests[number]()
    print()
