from yovirmac.modules.errors import *
from yovirmac.modules.segment_control import find
from yovirmac.modules.types_control import read


def list_segment(num):
    result = []
    while num != 0:
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        result += find.list_segment(num, last=last)
        num = next_num
    return result


def string_segment(num):
    result = ""
    while num != 0:
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        result += find.string_segment(num, last=last)
        num = next_num
    return result


def namespace(num):
    result = []
    while num != 0:
        next_num = find.attribute(num, "next_segment")
        last = True if next_num == 0 else False
        result += find.namespace(num, last=last)
        num = next_num
    return result


def list_segment_length(num):
    length = 0
    while num != 0:
        length += find.list_segment_length(num)
        num = find.attribute(num, "next_segment")
    return length


def string_segment_length(num):
    length = 0
    while num != 0:
        length += find.string_segment_length(num)
        num = find.attribute(num, "next_segment")
    return length


def list_segment_element(num, index):
    while num != 0:
        element_type, element = find.list_segment_element(num, index)
        if element_type == "link":
            return element_type, element
        index = element
        num = find.attribute(num, "next_segment")
    return "none", 0


def string_segment_element(num, index):
    while num != 0:
        element_type, element = find.string_segment_element(num, index)
        if element_type == "link":
            return element_type, element
        index = element
        num = find.attribute(num, "next_segment")
    return "none", 0


def namespace_element(num, key):
    while num != 0:
        value_type, value = find.namespace_key(num, key)
        if value_type is not None:
            return value_type, value


def namespace_key(num, key):
    data_begin, data_end = find.data_range(num)
    top = find.attribute(num, "first_full_cell")
    for i in range(data_begin, top, 2):
        item_type, item_value = read.entity(i)
        key_type, key_link = find.dictionary_item_key(item_value)
        key_value_type, key_value = entity(key_link)
        if key_value == key:
            value_type, value = find.dictionary_item_value(num)
            return value_type, value
    return None, None


def entity(num):
    kind = read.kind(num)
    if kind == "segment":
        kind = find.attribute(num, "type")
        if kind not in read_segment_dictionary:
            raise LowerCommandError(f"Неподдерживаемый тип сегмента для чтения"
                                    f" {kind}")
        return read_segment_dictionary[kind](num)
    else:
        return read.entity(num)


read_segment_dictionary = {
    "string_segment": string_segment,
    "list_segment": list_segment,
}
