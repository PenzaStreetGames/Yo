from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append, pull
from yovirmac.modules.types_control import write
from yovirmac.modules.segment_control import find, change


def Push(arg):
    arg_type, arg_value = arg
    if arg_type == "none":
        append.memory_stack("link", 0)
    elif arg_type == "number":
        num = append.data_segment("number", arg_value)
        append.memory_stack("link", num)
    else:
        raise UndefinedArgument(f"Поведение команды Psh с аргументом типа "
                                f"{arg_type} не определено")


def Pop(arg):
    arg_type, arg_value = arg
    if arg_type == "none":
        link_type, link = pull.memory_stack()
    elif arg_type == "link":
        link_type, link_value = pull.memory_stack()
        write.entity(arg_value, "link", link_value)
    else:
        raise UndefinedArgument(f"Поведение команды Pop с аргументом типа"
                                f"{arg_type} не определено")


def Call(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        target_cell = find.attribute(seg_links["system"], "target_cell")
        append.call_stack("link", target_cell + 4)
    else:
        raise UndefinedArgument(f"Поведение команды Cal с аргументом типа"
                                f"{arg_type} не определено")


def Return():
    link_type, target_cell = pull.call_stack()
    change.attribute(seg_links["system"], "target_cell", target_cell)
