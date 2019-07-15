from yovirmac.modules.tape_control import pull, get
from yovirmac.modules.types_control import display, read
from yovirmac.modules.segment_control import find
from yovirmac.modules.object_control import item


def entity_link(arg):
    display.entity(arg)


def entity(num):
    print(*get.entity(num))


def link_on_link(arg):
    link_type, link_value = arg
    link_type, str_link = read.entity(link_value)
    entity(str_link)


def memory_stack_link():
    entity(pull.memory_stack()[1])


def dictionary_item(num):
    key, value = item.get_dictionary_item(num)
    print(f"{key}: {value}")
