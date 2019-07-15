from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.segment_control import find
from yovirmac.modules.types_control import write, read
from yovirmac.modules.tape_control import get, append, make
from yovirmac.modules.object_control import link


def Sub_object(parent, index):
    par_type, par_value = parent
    ind_arg_type, ind_type, ind_value = link.unpack(index)
    if ind_type == "link":
        ind_type, ind_value = link.get_link(ind_value)
    if ind_type != "number":
        raise UndefinedBehaviour(f"Получение элемента командой Sob с индексом"
                                 f"типа {ind_type} не определено")
    if ind_value < 0:
        raise UndefinedBehaviour(f"Получение элемента командой Sob с "
                                 f"отрицательным индексом не определено")
    if par_type == "link":
        kind, link_value = read.entity(par_value)
        if kind == "link":
            kind = find.kind(link_value)
            par_value = link_value
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
        key = get.entity(arg_value)
        # потом: сделать механизм восходящего поиска
        seg_num = find.attribute(seg_links["system"], "target_namespace")
        res_type, res_num = get.namespace_element(seg_num, key)
        append.memory_stack("link", res_num)
    else:
        raise UndefinedArgument(f"Поведение команды Fnd с аргументом типа "
                                f"{arg_type} не определено")


def Create(arg):
    arg_type, arg_value = arg
    if arg_type == "none":
        res_num = append.data_segment(arg_type, arg_value)
    elif arg_type == "logic":
        res_num = append.data_segment(arg_type, arg_value)
    elif arg_type == "number":
        res_num = append.data_segment(arg_type, arg_value)
    elif arg_type == "chars":
        res_num = make.string_segment(arg_value)
    elif arg_type == "array":
        res_num = make.list_segment(arg_value)
    else:
        raise UndefinedArgument(f"Создание объекта командой Crt типа "
                                f"{arg_type} не определено")
    append.memory_stack("link", res_num)


def Equate(receiver, source):
    left_type, left_value = receiver
    if left_type != "link":
        raise UndefinedArgument(f"Приравнивание командой Eqt для приёмника "
                                f"типа {left_type} не определено")
    rec_type, rec_value = link.get_link(left_value)
    if rec_type != "link":
        raise UndefinedBehaviour(f"Приравнивание типа {rec_type} командой Eqt "
                                 f"не определено")
    right_type, right_value = source
    if right_type != "link":
        raise UndefinedArgument(f"Приравнивание командой Eqt для источника "
                                f"типа {right_type} не определено")
    src_type, src_value = link.get_link(right_value)
    if src_type == "link":
        obj_type, obj_value = link.get_link(src_value)
        copy_num = make.entity(obj_type, obj_value)
        write.entity(left_value, "link", copy_num)
    else:
        write.entity(left_value, "link", right_value)
    append.memory_stack("link", 0)
