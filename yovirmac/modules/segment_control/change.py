from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write, read
from yovirmac.modules.errors import *


def attribute(num, name, kind, value):
    base_args, args = read.segment(num + 2)
    segment_type = base_args["type"]
    header_part = find_header_part(name, segment_type)
    check_attribute_type(name, header_part, kind)
    index = calculate_index(num, name, header_part)
    write.entity(index, kind, value)


def find_header_part(name, seg_type):
    if name not in seg_header["basic"]:
        if name not in seg_header[seg_types[seg_type]]:
            raise LowerCommandError(
                f"Атрибут \"{name}\" отсутствует в заголовке сегмента")
        return seg_type
    else:
        return "basic"


def check_attribute_type(name, header_part, kind):
    real_type = seg_header_types[header_part][name]
    if kind != seg_header_types[header_part][name]:
        raise LowerCommandError(
            f"Атрибут \"{name}\" имеет тип \"{kind}\" вместо "
            f"\"{real_type}\"")


def calculate_index(num, name, header_part):
    if header_part == "basic":
        return num + 2 + seg_header[header_part].index(name) * 2
    else:
        return num + 2 + header_base_part_length + \
               seg_header[header_part].index(name) * 2
