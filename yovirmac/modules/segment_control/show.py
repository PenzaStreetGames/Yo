from yovirmac.modules.types_control import display, read, memory_control
from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.segment_control import find


def attribute(num, name):
    index, kind = find_attribute(num, name)
    display.entity(index)


def program_code(num):
    data_begin = find.attribute(num, "data_begin")
    index = data_begin
    obj_type, command = read.entity(index)
    while obj_type != "none":
        display.command_with_args(index)
        com_name, args = read.command_with_args(index)
        index += memory_control.determine_object_size("command_with_args", args)
        obj_type, command = read.entity(index)


def cells_stream(num):
    data_begin = find.attribute(num, "data_begin")
    data_end = find.attribute(num, "segment_end")
    for i in range(data_begin, data_end, 2):
        cells = [read.cell(i), read.cell(i + 1)]
        print(i, *cells)


def segment_body(num):
    data_begin, data_end = data_range(num)
    index = data_begin
    obj_type, obj_value = read.entity(index)
    while index < data_end and obj_type != "none":
        print(index, end=" ")
        display.entity(index)
        index += memory_control.determine_object_size(obj_type, obj_value)
        if index < data_end:
            obj_type, obj_value = read.entity(index)
    print()


def list_segment(num, last=False):
    print(find.list_segment(num, last=last))


def string_segment(num, last=False):
    print(find.string_segment(num, last=last))


def namespace(num, last=False):
    print(find.namespace(num, last=last))


def data_range(num):
    data_begin = find.attribute(num, "data_begin")
    data_end = find.attribute(num, "segment_end")
    return data_begin, data_end

