from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append


def negative(arg):
    obj_type, value = link.get(arg)
    if obj_type == "number":
        value = -value
        num = append.data_segment(obj_type, value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типа {obj_type} не определена операция "
                                f"инверсии Neg")
