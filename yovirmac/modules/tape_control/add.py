from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write, memory_control
from yovirmac.modules.segment_control import init, find, change
from yovirmac.modules.segment_control.init import get_min_size


def create_segment(seg_type, self_length=0):
    if seg_type != "system":
        num = get_last_cell()
    else:
        num = seg_links["system"]
    if self_length != 0:
        length = self_length + header_length
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
    cells = read_assembly(path)
    length = memory_control.determine_segment_size(len(cells))
    num = create_segment("program", self_length=length)
    # потом: сделать механизм проверки главности программы
    change.attribute(seg_links["system"], "main_program", num)
    stream_data(num, cells)


def get_last_cell():
    return find.attribute(seg_links["system"], "tape_length")


def tape_length(delta):
    length = find.attribute(seg_links["system"], "tape_length")
    change.attribute(seg_links["system"], "tape_length", length + delta)


def empty_data(num):
    first = num + header_length
    change.attribute(num, "data_begin", first)
    change.attribute(num, "first_empty_cell", first)


def stream_data(num, stream):
    first = num + header_length
    change.attribute(num, "data_begin", first)
    write.cells_stream(first, stream)
    change.attribute(num, "first_empty_cell", first + len(stream))


def read_assembly(path):
    with open(path, mode="rb") as assembly:
        cells = []
        target_cell = 0
        size = capacity // 8
        i = 0
        for cell in assembly.read():
            i += 1
            target_cell <<= 8
            target_cell += cell
            if i == size:
                cells += [target_cell]
                target_cell = 0
                i = 0
            cell = assembly.read(1)
    return cells
