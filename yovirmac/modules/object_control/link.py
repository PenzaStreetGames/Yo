from yovirmac.modules.errors import *
from yovirmac.modules.types_control import read
from yovirmac.modules.tape_control import pull


def get(link):
    return read.entity(link)


def memory_stack_get():
    kind, stack_link = pull.memory_stack()
    kind, number = get(stack_link)
    return kind, number


def unpack(arg):
    arg_type, arg_value = arg
    if arg_type != "link":
        raise LowerCommandError(f"Нельзя распаковать не-ссылку {arg_type}")
    obj_type, value = get(arg_value)
    return arg_type, obj_type, value
