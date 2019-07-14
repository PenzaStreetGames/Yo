from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.types_control import read


def attribute(num, name):
    index, kind = find_attribute(num, name)
    kind, value = read.entity(index)
    return value


def dictionary_item_key(num):
    return dictionary_item_part(num, "key")


def dictionary_item_value(num):
    return dictionary_item_part(num, "value")


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
    return kind, result


def kind(num):
    obj_kind = read.kind(num)
    if obj_kind == "segment":
        obj_kind = seg_types[attribute(num, "type")]
    return obj_kind


def list_segment(num, last=False):
    data_begin, data_end = data_range(num)
    if last:
        top = attribute(num, "first_empty_cell")
        data_end = top
    links = read.link_list(data_begin, data_end)
    return links


def string_segment(num, last=False):
    data_begin, data_end = data_range(num)
    if last:
        top = attribute(num, "first_empty_cell")
        data_end = top
    chars = read.char_list(data_begin, data_end)
    return chars


def namespace(num, last=False):
    data_begin, data_end = data_range(num)
    if last:
        top = attribute(num, "first_empty_cell")
        data_end = top
    links = read.link_list(data_begin, data_end)
    return links


def list_segment_length(num):
    begin = attribute(num, "data_begin")
    end = attribute(num, "segment_end")
    top = attribute(num, "first_empty_cell")
    if top == end:
        return (end - begin) // 2
    else:
        return (top - begin) // 2


def string_segment_length(num):
    begin = attribute(num, "data_begin")
    end = attribute(num, "segment_end")
    top = attribute(num, "first_empty_cell")
    if top == end:
        return (end - begin) // 2
    else:
        return (top - begin) // 2


def list_segment_element(num, index):
    length = list_segment_length(num)
    data_begin, data_end = data_range(num)
    if length >= index:
        entity_index = data_begin + (index - 1) * 2
        return "link", entity_index
    else:
        return "none", index - length


def string_segment_element(num, index):
    length = string_segment_length(num)
    data_begin, data_end = data_range(num)
    if length >= index:
        entity_index = data_begin + (index - 1) * 2
        return "link", entity_index
    else:
        return "none", index - length


def data_range(num):
    data_begin = attribute(num, "data_begin")
    data_end = attribute(num, "segment_end")
    return data_begin, data_end


def is_full(num):
    top = attribute(num, "first_empty_cell")
    end = attribute(num, "segment_end")
    if top == end:
        return True
    return False


def is_last(num):
    next_segment = attribute(num, "next_segment")
    if next_segment == 0:
        return True
    return False

