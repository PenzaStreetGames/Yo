from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import memory_control
from yovirmac.modules.tape_control import add, append
from yovirmac.modules.segment_control import put


def string_segment(data):
    data_size = memory_control.determine_object_size("char_list", data)
    seg_size = memory_control.determine_segment_size(data_size)
    num = add.string_segment(self_length=seg_size)
    put.string_segment(num, "char_list", data)
    return num


def list_segment(data):
    data_size = memory_control.determine_object_size("link_list", data)
    seg_size = memory_control.determine_segment_size(data_size)
    num = add.list_segment(self_length=seg_size)
    put.list_segment(num, "link_list", data)
    return num


def entity(obj_type, value):
    if obj_type == "string":
        num = string_segment(value)
    elif obj_type == "list":
        num = list_segment(value)
    elif obj_type in types:
        num = append.data_segment(obj_type, value)
    else:
        raise LowerCommandError(f"Неподдерживаемый тип для сегментной записи"
                                f" {obj_type}")
    return num
