from yovirmac.modules.constants import *
from yovirmac.modules.segment_control import find, put


def memory_stack(obj_type, value):
    mem_num = find.attribute(seg_links["system"], "memory_stack")
    put.stack(mem_num, obj_type, value)


def call_stack(obj_type, value):
    call_num = find.attribute(seg_links["system"], "call_stack")
    put.stack(call_num, obj_type, value)


def data_segment(obj_type, value):
    data_num = find.attribute(seg_links["system"], "first_data_segment")
    num = put.data_segment(data_num, obj_type, value)
    return num
