from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.segment_control import find
from yovirmac.modules.types_control import read
from yovirmac.modules.tape_control import get, append
from yovirmac.modules.object_control import link


def Subobject(parent, index):
    par_type, par_value = parent
    ind_arg_type, ind_type, ind_value = link.unpack(index)
    if ind_type != "number":
        raise UndefinedBehaviour(f"Получение элемента командой Sob с индексом"
                                 f"типа {ind_type} не определено")
    if ind_value < 0:
        raise UndefinedBehaviour(f"Получение элемента командой Sob с "
                                 f"отрицательным индексом не определено")
    if par_type == "link":
        kind = find.kind(par_value)
        if kind == "string_segment":
            elem_type, elem_value = get.string_segment_element(par_value,
                                                               ind_value)
        elif kind == "list_segment":
            elem_type, elem_value = get.list_segment_element(par_value,
                                                             ind_value)
        else:
            raise UndefinedBehaviour(f"Получение элемента командой Sob для "
                                     f"типа {kind} не определено")
        if elem_type == "none":
            num = append.data_segment("none", 0)
            append.memory_stack("link", num)
        elif elem_type == "link":
            append.memory_stack("link", elem_value)
        else:
            raise LowerCommandError(f"Поиск элемента не может возращать объект"
                                    f"типа {elem_type}")
    else:
        raise UndefinedArgument(f"Поведение команды Sob с аргументом типа"
                                f"{par_type} не определено")


def Length(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        kind = find.kind(arg_value)
        if kind == "string_segment":
            length = get.string_segment_length(arg_value)
        elif kind == "list_segment":
            length = get.list_segment_length(arg_value)
        else:
            raise UndefinedBehaviour(f"Получение длины командой Len для "
                                     f"типа {kind} не определено")
        num = append.data_segment("number", length)
        append.memory_stack("link", num)
    else:
        raise UndefinedArgument(f"Поведение команды Len с аргументом типа "
                                f"{arg_type} не определено")


def Find(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        seg_num = find.attribute(seg_links["system"], "target_namespace")

    else:
        raise UndefinedArgument(f"Поведение команды Fnd с аргументом типа "
                                f"{arg_type} не определено")
