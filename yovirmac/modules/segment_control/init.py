from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write
from yovirmac.modules.segment_control import change


def segment(num, seg_type, length):
    base_args = {}
    if type(seg_type) == int:
        if not (0 <= seg_type < len(seg_types)):
            raise LowerCommandError(f"Неподдерживаемый индекс типа"
                                    f"сегмента: {seg_type}")
        base_args["type"] = seg_type
    elif type(seg_type) == str:
        if seg_type not in seg_types:
            raise LowerCommandError(f"Неизвестный тип сегмента: {seg_type}")
        base_args["type"] = seg_types.index(seg_type)
    base_args["length"] = length
    write.segment(num, base_args, {})
    # запись ссылки на конец сегмента
    change.attribute(num, "segment_end", num + length)


def get_min_size(kind):
    if type(kind) == int:
        return header_length + minimal_data_length[seg_types[kind]]
    elif type(kind) == str:
        return header_length + minimal_data_length[kind]
