from yovirmac.modules.constants import *
from yovirmac.modules.segment_control import init, find, change
from yovirmac.modules.segment_control.init import get_min_size


def system_area():
    length = get_min_size("system")
    init.segment(seg_links["system"], "system", length=length)
    tape_length(length)


def memory_stack():
    num = get_last_cell()
    length = get_min_size("memory_stack")
    init.segment(num, "memory_stack", length=length)
    change.attribute(seg_links["system"], "memory_stack", num)
    empty_data(num)
    tape_length(length)


def call_stack():
    num = get_last_cell()
    length = get_min_size("call_stack")
    init.segment(num, "call_stack", length=length)
    change.attribute(seg_links["system"], "call_stack", num)
    empty_data(num)
    tape_length(length)


def get_last_cell():
    return find.attribute(seg_links["system"], "tape_length")


def tape_length(delta):
    length = find.attribute(seg_links["system"], "tape_length")
    change.attribute(seg_links["system"], "tape_length", length + delta)


def empty_data(num):
    first = num + header_length
    change.attribute(num, "data_begin", first)
    change.attribute(num, "first_empty_cell", first)
