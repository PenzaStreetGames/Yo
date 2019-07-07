from yovirmac.modules.segment_control.functions import *
from yovirmac.modules.types_control import read


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
