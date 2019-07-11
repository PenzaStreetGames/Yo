from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write, memory_control
from yovirmac.modules.segment_control import find, change
from yovirmac.modules.tape_control import extend
from yovirmac.modules.segment_control.functions import *


def stack(num, obj_type, value):
    check_type("stack", obj_type)
    obj_size = memory_control.determine_object_size(obj_type, value)
    top = find.attribute(num, "first_empty_cell")
    place = check_free_place(num, obj_size)
    check_stack_overflow(num, place)
    write.entity(top, obj_type, value)
    change_stack(num, top + obj_size, top, place)


def data_segment(num, obj_type, value):
    top = find.attribute(num, "first_empty_cell")
    obj_size = memory_control.determine_object_size(obj_type, value)
    place = check_free_place(num, obj_size)
    if place >= 0:
        write.entity(top, obj_type, value)
        change_data(num, top + obj_size, place)
        index = top
    else:
        if not is_last(num):
            next_num = find.attribute(num, "next_segment")
            index = data_segment(next_num, obj_type, value)
        else:
            new_num = extend.data_segment(num)
            index = data_segment(new_num, obj_type, value)
    return index


def list_segment(num, obj_type, value):
    check_type("list", obj_type)
    last_num = get_last(num)
    obj_size = memory_control.determine_object_size(obj_type, value)
    top = find.attribute(last_num, "first_empty_cell")
    place = check_free_place(last_num, obj_size)
    if place >= 0:
        write.link_list(top, value)
        change_data(last_num, top + obj_size, place)
    else:
        part_1, part_2 = split_cells(obj_size, place, value)
        write.link_list(top, part_1)
        new_num = extend.list_segment(last_num)
        list_segment(num, obj_type, part_2)


def namespace(num, obj_type, value):
    check_type("namespace", obj_type)
    last_num = get_last(num)
    obj_size = memory_control.determine_object_size(obj_type, value)
    top = find.attribute(last_num, "first_empty_cell")
    place = check_free_place(last_num, obj_size)
    if place >= 0:
        write.link_list(top, value)
        change_data(last_num, top + obj_size, place)
    else:
        part_1, part_2 = split_cells(obj_size, place, value)
        write.link_list(top, part_1)
        new_num = extend.namespace(last_num)
        namespace(num, obj_type, part_2)


def string_segment(num, obj_type, value):
    check_type("string", obj_type)
    last_num = get_last(num)
    obj_size = memory_control.determine_object_size(obj_type, value)
    top = find.attribute(last_num, "first_empty_cell")
    place = check_free_place(last_num, obj_size)
    if place >= 0:
        write.char_list(top, value)
        change_data(last_num, top + obj_size, place)
    else:
        part_1, part_2 = split_cells(obj_size, place, value)
        write.char_list(top, part_1)
        new_num = extend.string_segment(last_num)
        string_segment(num, obj_type, part_2)


def check_type(seg_type, obj_type):
    if seg_type == "stack" and obj_type != "link":
        raise LowerCommandError(f"Стеки хранят только ссылки, а не "
                                f"{obj_type}")
    elif seg_type == "list" and obj_type != "link_list":
        raise LowerCommandError(f"Списки хранят только ссылки, а не "
                                f"{obj_type}")
    elif seg_type == "namespace" and obj_type != "link_list":
        raise LowerCommandError(f"Пространства имён хранят только ссылки, а не "
                                f"{obj_type}")
    elif seg_type == "string" and obj_type != "char_list":
        raise LowerCommandError(f"Строки хранят только символы, а не "
                                f"{obj_type}")


def check_stack_overflow(num, place):
    if place < 0:
        stack_type = find.attribute(num, "type")
        raise LowerCommandError(f"Стек {seg_types[stack_type]} переполнен")


def check_free_place(num, obj_size):
    free_cells = find.attribute(num, "free_cells")
    place = free_cells - obj_size
    return place


def get_last(num):
    if not is_last(num):
        next_num = find.attribute(num, "next_segment")
        last_num = get_last(next_num)
    else:
        last_num = num
    return last_num


def is_last(num):
    next_segment = find.attribute(num, "next_segment")
    if next_segment == 0:
        return True
    return False


def split_cells(obj_size, place, value):
    point = obj_size - abs(place)
    part_1 = value[:point]
    part_2 = value[point:]
    return part_1, part_2
