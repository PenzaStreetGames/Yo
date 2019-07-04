from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write, read
from yovirmac.modules.errors import *


def attribute(num, name, type_and_value):
    base_args, args = read.segment(num)
    kind, value = type_and_value
    segment_type = base_args["type"]
    if name not in seg_header["basic"]:
        if name not in seg_header[seg_types[segment_type]]:
            raise LowerCommandError(
                f"Атрибут \"{name}\" отсутствует в заголовке сегмента")
        real_type = seg_header_types[segment_type]
        if kind != seg_header_types[segment_type][name]:
            raise LowerCommandError(
                f"Атрибут \"{name}\" имеет тип \"{kind}\" вместо \"{}\"")
        index = num + header_base_part_length + seg_header[
            segment_type].index(name) * 2
        write.entity()