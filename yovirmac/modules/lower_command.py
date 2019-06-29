from yovirmac.modules.constants import *








def clean_cell(cell):
    memory[cell] = 0


def add_cells(number):
    global memory
    memory += [0] * number


def bit_left_shift(cell, shift):
    global memory
    memory[cell] <<= shift
    memory[cell] &= full_cell


def bit_right_shift(cell, shift):
    global memory
    memory[cell] >>= shift





def write_value(cell, value_type, value):
    if type(value_type) == int:
        str_type = types[value_type]
    else:
        str_type = value_type
    write_type(cell, value_type)
    value_cell = cell + 1
    if str_type == "none":
        write_none(value_cell)
    elif str_type == "link":
        write_link(value_cell, value)
    elif str_type == "command":
        pass  # надо: написать функции write/read/print_command
    elif str_type == "logic":
        write_logic(value_cell, value)
    elif str_type == "number":
        write_number(value_cell, value)
    elif str_type == "string":
        write_string(value_cell, value)
    elif str_type == "segment":
        pass  # надо: написать функции write/read/print_segment
    else:
        pass  # надо: выдать в этом месте ошибку


def write_segment(cell, type):
    pass


def write_segment_header(cell):
    pass


def write_segment_base_header(cell):
    pass


def write_segment_special_header(cell):
    pass
