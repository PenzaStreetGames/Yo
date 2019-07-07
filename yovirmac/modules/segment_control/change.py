from yovirmac.modules.constants import *
from yovirmac.modules.types_control import write, read
from yovirmac.modules.errors import *
from yovirmac.modules.segment_control.functions import *


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
