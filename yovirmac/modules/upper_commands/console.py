from yovirmac.modules.errors import *
from yovirmac.modules.tape_control import make, append, get
from yovirmac.modules.object_control import link


def Input():
    value = input()
    num = make.string_segment(value)
    append.memory_stack("link", num)


def Output(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        value = get.string_segment(arg_value)
        print(value)
    else:
        raise LowerCommandError(f"Поведение команды Out с аргументом типа"
                                f"{arg_type} не определено")
