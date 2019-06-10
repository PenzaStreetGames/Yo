from yovirmac.modules.tests import *

tests = [
    cell_overflow_write,
    cell_overflow_shift,
    bit_write,
    number_write,
]

while True:
    number = int(input())
    print(tests[number].__doc__)
    tests[number]()
    print()
