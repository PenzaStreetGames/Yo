from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write, memory_control
from yovirmac.modules.segment_control import find, change
from yovirmac.modules.tape_control import extend
from yovirmac.modules.segment_control.functions import *


def stack(num, obj_type, value):
    check_link_type(obj_type)
    obj_size = memory_control.determine_object_size(obj_type, value)
    top = find.attribute(num, "first_empty_cell")
    place = check_free_place(num, obj_size)
    check_stack_overflow(num, place)
    write.entity(top, obj_type, value)
    change_stack(num, top + obj_size, top, place)


def data_segment(num, obj_type, value, begin=True):
    top = find.attribute(num, "first_empty_cell")
    if begin:
        obj_size = memory_control.determine_object_size(obj_type, value)
        place = check_free_place(num, obj_size)
        if place >= 0:
            write.entity_part(top, obj_type, value, begin=True, end=True)
            change_data(num, top + obj_size, place)
        else:
            part_1, part_2 = split_to_parts(place, obj_type, value, begin)
            write.entity_part(top, obj_type, part_1, begin=True, end=False)
            change.attribute(num, "interrupt", 1)
            new_num = extend.data_segment(num)
            data_segment(new_num, obj_type, part_2, begin=False)
    else:
        obj_size = memory_control.determine_value_size(obj_type, value)
        place = check_free_place(num, obj_size)
        if place >= 0:
            write.entity_part(top, obj_type, value, begin=False, end=True)
            change_data(num, top + obj_size, place)
        else:
            part_1, part_2 = split_to_parts(place, obj_type, value, begin)
            write.entity_part(top, obj_type, part_1, begin=False, end=False)
            change.attribute(num, "interrupt", 1)
            new_num = extend.data_segment(num)
            data_segment(new_num, obj_type, part_2, begin=False)


def check_link_type(obj_type):
    if obj_type != "link":
        raise LowerCommandError(f"Стеки хранят только ссылки, а не "
                                f"{obj_type}")


def check_stack_overflow(num, place):
    if place < 0:
        stack_type = find.attribute(num, "type")
        raise LowerCommandError(f"Стек {seg_types[stack_type]} переполнен")


def check_free_place(num, obj_size):
    free_cells = find.attribute(num, "free_cells")
    place = free_cells - obj_size
    return place


def split_to_parts(place, obj_type, value, begin):
    if obj_type == "string":
        if begin:
            # ситуация end=True невозможна нет смысла делить помещающийся объект
            point = place - 1
        else:
            # ситуация end=True невозможна нет смысла делить завершённый объект
            point = place
    elif obj_type == "dictionary_item":
        if begin:
            point = place // 2 - 1
        else:
            point = place // 2
    else:
        raise LowerCommandError(f"Для типа {obj_type} не предусмотрен "
                                f"межсегментный перенос")
    part_1 = value[:point]
    part_2 = value[point:]
    return part_1, part_2

