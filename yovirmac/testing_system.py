from yovirmac.modules.tests import *

tests = {
    1: cell_overflow_write,
    2: cell_overflow_shift,
    3: bit_writing,
    4: number_writing,
    5: type_writing,
}

add_cells(64)
while True:
    number = int(input())
    print(tests[number].__doc__)
    tests[number]()
    print()
