from yovirmac.modules.types_control import memory_control
from yovirmac.modules.tape_control import add
from yovirmac.modules.segment_control import put


def string_segment(data):
    data_size = memory_control.determine_segment_size(len(data))
    num = add.string_segment(self_length=data_size)
    put.string_segment(num, "char_list", data)
    return num


def list_segment(data):
    data_size = memory_control.determine_segment_size(len(data))
    num = add.list_segment(self_length=data_size)
    put.list_segment(num, "link_list", data)
    return num
