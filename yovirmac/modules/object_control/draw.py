from yovirmac.modules.tape_control import pull
from yovirmac.modules.types_control import display


def entity_link(arg):
    display.entity(arg)


def memory_stack_link():
    display.entity(pull.memory_stack()[1])
