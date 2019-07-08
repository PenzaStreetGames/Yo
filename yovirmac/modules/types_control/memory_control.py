from yovirmac.modules.constants import *
import math


def add_cells(number):
    global memory
    memory += [0] * number


def determine_object_size(obj_type, value):
    if type(types_length[obj_type]) == int:
        return types_length[obj_type]
    elif obj_type == "string":
        if len(value) % 2 == 1:
            return len(value) + 3
        else:
            return len(value) + 2
    elif obj_type == "array":
        return len(value) * 2 + 4
    elif obj_type == "command_with_args":
        size = 2
        for arg in value:
            arg_type, arg_value = arg["type"], arg["value"]
            size += determine_object_size(arg_type, arg_value)
        return size


def determine_segment_size(length):
    indicator = math.ceil(math.log2(length))
    return 2 ** indicator
