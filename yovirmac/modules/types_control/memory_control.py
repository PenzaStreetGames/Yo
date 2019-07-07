from yovirmac.modules.constants import *
import math


def add_cells(number):
    global memory
    memory += [0] * number


def determine_object_size(obj_type, value):
    if type(types_length[obj_type]) == int:
        return types_length[obj_type]
    elif obj_type == "string":
        if value % 2 == 1:
            return len(value) + 3
        else:
            return len(value) + 2


def determine_segment_size(length):
    indicator = math.ceil(math.log2(length))
    return 2 ** indicator
