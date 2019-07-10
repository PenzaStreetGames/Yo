from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.types_control import read
from yovirmac.modules.segment_control import find


def attribute(num, name):
    index, kind = find_attribute(num, name)
    kind, value = read.entity(index)
    return value


def dictionary_item_part(num, part):
    if part == "dictionary":
        kind, result = read.entity(num + 2)
    elif part == "key":
        kind, result = read.entity(num + 4)
    elif part == "value":
        kind, result = read.entity(num + 6)
    else:
        raise LowerCommandError(f"Несуществующий атрибут элемента словаря "
                                f"{part}")


def data_segment_entity(seg_num, num, begin=True, obj_type=None,
                        past_data=None):
    segment_end = find.attribute(seg_num, "segment_end")
    if begin:
        obj_type, value, end = read.entity_part(num, stop=segment_end - 1,
                                                begin=True)
    else:
        obj_type, value, end = read.entity_part(num, stop=segment_end - 1,
                                                begin=False, obj_type=obj_type,
                                                past_data=past_data)
    if not end:
        next_segment = find.attribute(seg_num, "next_segment")
        data_begin = find_attribute(next_segment, "data_begin")
        obj_type, delta_value = data_segment_entity(
            next_segment, data_begin, begin=False, obj_type=obj_type,
            past_data=value)
        value += delta_value
    return obj_type, value
