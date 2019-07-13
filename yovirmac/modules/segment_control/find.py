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
        return end - begin
    else:
        return top - begin


def string_segment_length(num):
    begin = attribute(num, "data_begin")
    end = attribute(num, "segment_end")
    top = attribute(num, "first_empty_cell")
    if top == end:
        return end - begin
    else:
        return top - begin


def list_element(num, index):
    data_begin, data_end = data_range(num)
    data_length = data_end - data_begin
    # надо: дописать эту функцию


def data_range(num):
    data_begin = attribute(num, "data_begin")
    data_end = attribute(num, "segment_end")
    return data_begin, data_end


def is_full(num):
    top = find.attribute(num, "first_empty_cell")
    end = find.attribute(num, "segment_end")
    if top == end:
        return True
    return False
