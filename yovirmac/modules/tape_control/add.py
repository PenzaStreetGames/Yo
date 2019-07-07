from yovirmac.modules.constants import *
from yovirmac.modules.segment_control import init, find, change
from yovirmac.modules.segment_control.init import get_min_size


def create_segment(seg_type, self_length=0):
    if seg_type != "system":
        num = get_last_cell()
    else:
        num = seg_links["system"]
    if self_length != 0:
        length = self_length
    else:
        length = get_min_size(seg_type)
    init.segment(num, seg_type, length=length)
    tape_length(length)
    return num


def system_area():
    create_segment("system")


def memory_stack():
    num = create_segment("memory_stack")
    change.attribute(seg_links["system"], "memory_stack", num)
    empty_data(num)


def call_stack():
    num = create_segment("call_stack")
    change.attribute(seg_links["system"], "call_stack", num)
    empty_data(num)


def data_segment():
    num = create_segment("data_segment")
    change.attribute(seg_links["system"], "first_data_segment", num)
    change.attribute(seg_links["system"], "last_data_segment", num)
    empty_data(num)


def program(path):
    with open(path, mode="rb") as assembly:
        res = []
        target_cell = 0
        size = capacity // 8
        i = 0
        cell = assembly.read(1)
        while cell:
            i += 1
            target_cell <<= 8
            target_cell += int(cell)
            if i == size:
                res += [target_cell]
                target_cell = 0
                i = 0
            cell = assembly.read(1)
    return res


def get_last_cell():
    return find.attribute(seg_links["system"], "tape_length")


def tape_length(delta):
    length = find.attribute(seg_links["system"], "tape_length")
    change.attribute(seg_links["system"], "tape_length", length + delta)


def empty_data(num):
    first = num + header_length
    change.attribute(num, "data_begin", first)
    change.attribute(num, "first_empty_cell", first)
