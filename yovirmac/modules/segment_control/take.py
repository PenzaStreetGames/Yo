from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.types_control import write, memory_control
from yovirmac.modules.segment_control import find, change
from yovirmac.modules.segment_control.functions import *


def stack(num):
    top = find.attribute(num, "first_empty_cell")
    data_begin = find.attribute(num, "data_begin")
    if top == data_begin:
        stack_type = find.attribute(num, "type")
        raise LowerCommandError(f"Стек {seg_types[stack_type]} пуст при "
                                f"попытке извлечения")
    last_cell = find.attribute(num, "last_full_cell")
    free_cells = find.attribute(num, "free_cells")
    obj_type, obj_value = read.entity(last_cell)
    write.entity(last_cell, "none", None)
    change_stack(num, top - types_length["link"],
                 last_cell - types_length["link"],
                 free_cells + types_length["link"])
    return obj_type, obj_value
