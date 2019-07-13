from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append, pull
from yovirmac.modules.types_control import write
from yovirmac.modules.segment_control import find, change


def Jump(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        change.attribute(seg_links["system"], "target_cell", arg_value)
    else:
        raise LowerCommandError(f"Поведение команды Jmp с аргументом типа"
                                f"{arg_type} не определено")


def Jump_if(arg, condition):
    arg_type, arg_value = arg
    cond_arg_type, cond_type, cond_value = link.unpack(condition)
    if arg_type == "link":
        if cond_type == "logic":
            if cond_value:
                change.attribute(seg_links["system"], "target_cell", arg_value)
        else:
            raise LowerCommandError(f"Поведение команды Jif с аргументами типов"
                                    f"{arg_type} и {cond_type} не определено")
    else:
        raise LowerCommandError(f"Поведение команды Jif с аргументом типа"
                                f"{arg_type} не определено")


def End():
    change.attribute(seg_links["system"], "target_cell", 0)
