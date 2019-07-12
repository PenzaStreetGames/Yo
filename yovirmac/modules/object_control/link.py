from yovirmac.modules.types_control import read
from yovirmac.modules.tape_control import pull


def get(link):
    return read.entity(link)


def memory_stack_get():
    kind, stack_link = pull.memory_stack()
    kind, number = get(stack_link)
    return kind, number
