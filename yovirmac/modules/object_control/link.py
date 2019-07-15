from yovirmac.modules.errors import *
from yovirmac.modules.tape_control import pull, get


def get_link(link):
    return get.entity(link)


def memory_stack_get():
    kind, stack_link = pull.memory_stack()
    kind, number = get_link(stack_link)
    return kind, number


def unpack(arg):
    arg_type, arg_value = arg
    if arg_type != "link":
        raise UndefinedArgument(f"Нельзя распаковать не-ссылку {arg_type}")
    obj_type, value = get_link(arg_value)
    return arg_type, obj_type, value
