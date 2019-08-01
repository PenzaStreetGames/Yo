from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
import math


def add_cells(number):
    global memory
    memory += [0] * number


def determine_object_size(obj_type, value):
    if type(types_length[obj_type]) == int:
        return types_length[obj_type]
    elif obj_type == "chars":
        if len(value) % 2 == 1:
            return len(value) + 3
        else:
            return len(value) + 2
    elif obj_type == "char_list":
        return len(value) * 2
    elif obj_type == "link_list":
        return len(value) * 2
    elif obj_type == "array":
        return len(value) * 2 + 4
    elif obj_type == "command_with_args":
        size = 2
        for arg in value:
            arg_type, arg_value = arg
            size += determine_object_size(arg_type, arg_value)
        return size
    raise LowerCommandError(f"Для типа {obj_type} нет метода определения "
                            f"размера объекта")


def determine_segment_size(seg_type, length):
    if length != 0:
        indicator = math.ceil(math.log2(length))
        if 2 ** indicator < minimal_data_length[seg_type]:
            return minimal_data_length[seg_type]
        return 2 ** indicator
    else:
        return minimal_data_length[seg_type]
