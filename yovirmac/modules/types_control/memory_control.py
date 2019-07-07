from yovirmac.modules.constants import *


def add_cells(number):
    global memory
    memory += [0] * number


def determine_size(obj_type, value):
    if type(types_length[obj_type]) == int:
        return types_length[obj_type]
    elif obj_type == "string":
        if value % 2 == 1:
            return len(value) + 3
        else:
            return len(value) + 2
