from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write, memory_control
from yovirmac.modules.segment_control import find, change
from yovirmac.modules.segment_control.functions import *


def stack(num, obj_type, value):
    check_link_type(obj_type)
    obj_size = memory_control.determine_object_size(obj_type, value)
    top = find.attribute(num, "first_empty_cell")
    place = check_free_place(num, obj_size)
    check_overflow(num, place)
    write.entity(top, obj_type, value)
    change_stack(num, top + obj_size, top, place)


def check_link_type(obj_type):
    if obj_type != "link":
        raise LowerCommandError(f"Стеки хранят только ссылки, а не "
                                f"{obj_type}")


def check_overflow(num, place):
    if place < 0:
        stack_type = find.attribute(num, "type")
        raise LowerCommandError(f"Стек {seg_types[stack_type]} переполнен")


def check_free_place(num, obj_size):
    free_cells = find.attribute(num, "free_cells")
    place = free_cells - obj_size
    return place
