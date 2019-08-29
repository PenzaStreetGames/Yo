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
    return seg_links["system"]


def memory_stack():
    num = create_segment("memory_stack")
    change.attribute(seg_links["system"], "memory_stack", num)
    empty_data(num)
    return num


def call_stack():
    num = create_segment("call_stack")
    change.attribute(seg_links["system"], "call_stack", num)
    empty_data(num)
    return num


def data_segment():
    num = create_segment("data_segment")
    change.attribute(seg_links["system"], "first_data_segment", num)
    change.attribute(seg_links["system"], "last_data_segment", num)
    empty_data(num)
    return num


def program(path):
    cells = read_assembly(path)
    length = memory_control.determine_segment_size("program", len(cells))
    num = create_segment("program", self_length=length)
    # потом: сделать механизм проверки главности программы
    change.attribute(seg_links["system"], "main_program", num)
    data_begin = stream_data(num, cells)
    change.attribute(seg_links["system"], "target_cell", data_begin)
    change.relative_links(num)
    namespace(num)
    return num


def namespace(program_num):
    num = create_segment("namespace")
    change.attribute(num, "program", program_num)
    change.attribute(program_num, "namespace", num)
    # потом: сделать механизм проверки главности пространства имён
    change.attribute(seg_links["system"], "target_namespace", num)
    empty_data(num)
    return num


def list_segment(self_length=0):
    num = create_segment("list_segment", self_length=self_length)
    empty_data(num)
    return num


def string_segment(self_length=0):
    num = create_segment("string_segment", self_length=self_length)
    empty_data(num)
    return num


def get_last_cell():
    return find.attribute(seg_links["system"], "tape_length")


def tape_length(delta):
    length = find.attribute(seg_links["system"], "tape_length")
    change.attribute(seg_links["system"], "tape_length", length + delta)


def empty_data(num):
    first = num + header_length
    change.attribute(num, "data_begin", first)
    change.attribute(num, "first_empty_cell", first)
    seg_end = find.attribute(num, "segment_end")
    change.attribute(num, "free_cells", seg_end - first)


def stream_data(num, stream):
    first = num + header_length
    change.attribute(num, "data_begin", first)
    write.cells_stream(first, stream)
    change.attribute(num, "first_empty_cell", first + len(stream))
    return first


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
