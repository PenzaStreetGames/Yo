from yovirmac.modules.tape_control import pull, get
from yovirmac.modules.types_control import display, read
from yovirmac.modules.segment_control import find
from yovirmac.modules.object_control import item, to_string
from yovirmac.modules.constants import *
from yovirmac.modules.errors import *


def entity_link(arg):
    display.entity(arg)


def entity(num):
    kind, value = get.entity(num)
    if kind in seg_types:
        if kind in seg_visible_types:
            if kind == "list_segment":
                print(to_string.list_segment(value))
            print(value)
        else:
            raise LowerCommandError(f"Неотображаемый тип сегмента {kind}")
    else:
        return display.entity(num)


def link_on_link(arg):
    link_type, link_value = arg
    link_type, str_link = read.entity(link_value)
    entity(str_link)


def memory_stack_link():
    entity(pull.memory_stack()[1])


def dictionary_item(num):
    key, value = item.get_dictionary_item(num)
    print(f"{key}: {value}")

