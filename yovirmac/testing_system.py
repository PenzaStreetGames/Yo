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
    12: attribute_writing,
    13: stack_writing,
    14: dictionary_item_writing,
    15: data_segment_writing,
    16: program_writing,
    17: array_writing,
    18: command_with_args_writing,
    19: list_segment_writing,
    20: segment_extending,
    21: stack_taking_putting,
    22: data_segment_putting,
    23: string_segment_putting,
    24: list_segment_putting,
    25: namespace_putting,
    26: list_and_string_segments_making,
    27: negative_number_writing,
    28: negative_command_working,
    29: math_operations_working,
    30: logic_operations_working,
    31: comparison_operations_working,
    32: memory_stack_operations_working,
    33: jumps_operations_working,
    34: console_operations_working,
}

memory_control.add_cells(64)
while True:
    number = int(input())
    print(tests[number].__doc__)
    tests[number]()
    print()
