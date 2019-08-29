from yovirmac.modules.constants import *
from yovirmac.modules.segment_control import find, take


def memory_stack():
    mem_num = find.attribute(seg_links["system"], "memory_stack")
    return take.stack(mem_num)


def call_stack():
    call_num = find.attribute(seg_links["system"], "call_stack")
    return take.stack(call_num)
