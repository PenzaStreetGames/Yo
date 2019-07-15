from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write, read, memory_control
from yovirmac.modules.errors import *
from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.segment_control import find


def attribute(num, name, value):
    index, kind = find_attribute(num, name)
    write.entity(index, kind, value)


def dictionary_item_part(num, part, value):
    if part == "dictionary":
        write.entity(num + 2, "link", value)
    elif part == "key":
        write.entity(num + 4, "link", value)
    elif part == "value":
        write.entity(num + 6, "link", value)
    else:
        raise LowerCommandError(f"Несуществующий атрибут элемента словаря "
                                f"{part}")


def relative_links(num):
    data_begin = find.attribute(num, "data_begin")
    data_end = find.attribute(num, "segment_end")
    index = data_begin
    while index < data_end:
        obj_type, obj_value = read.entity(index)
        if obj_type == "link":
            write.entity(index, "link", data_begin + obj_value)
            index += memory_control.determine_object_size(obj_type, obj_value)
        elif obj_type == "chars":
            index += memory_control.determine_object_size(obj_type, obj_value)
        else:
            index += 2


def target_cell(cell, args):
    command_size = memory_control.determine_object_size("command_with_args",
                                                        args)
    cell += command_size
    attribute(seg_links["system"], "target_cell", cell)
