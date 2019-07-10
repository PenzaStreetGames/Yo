from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
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
    raise LowerCommandError(f"Для типа {obj_type} нет метода определения "
                            f"размера объекта")


def determine_value_size(obj_type, value):
    if type(types_length[obj_type]) == 2:
        return 1
    elif obj_type == "dictionary_item":
        return len(value) * 2
    elif obj_type == "string":
        if len(value) % 2 == 1:
            return len(value) + 1
        else:
            return len(value) + 2
    elif obj_type == "array":
        return len(value) + 2
    raise LowerCommandError(f"Для типа {obj_type} нет метода для определения "
                            f"размера величины")


def determine_segment_size(length):
    indicator = math.ceil(math.log2(length))
    return 2 ** indicator
