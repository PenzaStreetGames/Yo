from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import read, memory_control
from yovirmac.modules.segment_control import change


def find_attribute(num, name):
    base_args, args = read.segment(num)
    segment_type = base_args["type"]
    header_part = find_header_part(name, segment_type)
    kind = seg_header_types[header_part][name]
    index = calculate_index(num, name, header_part)
    return index, kind


def find_header_part(name, seg_type):
    if name not in seg_header["basic"]:
        if name not in seg_header[seg_types[seg_type]]:
            raise LowerCommandError(
                f"Атрибут \"{name}\" отсутствует в заголовке сегмента")
        return seg_types[seg_type]
    else:
        return "basic"


def calculate_index(num, name, header_part):
    if header_part == "basic":
        return num + 2 + seg_header[header_part].index(name) * 2
    else:
        return num + 2 + header_base_part_length + \
               seg_header[header_part].index(name) * 2


def change_stack(num, first_empty_cell_value, last_full_cell_value,
                 free_cells_value):
    change.attribute(num, "first_empty_cell", first_empty_cell_value)
    change.attribute(num, "last_full_cell", last_full_cell_value)
    change.attribute(num, "free_cells", free_cells_value)


def change_data(num, first_empty_cell_value, free_cells_value):
    change.attribute(num, "first_empty_cell", first_empty_cell_value)
    change.attribute(num, "free_cells", free_cells_value)
