from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.segment_control import find
from yovirmac.modules.types_control import read
from yovirmac.modules.tape_control import get, append


def Subobject(parent, index):
    pass


def Length(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        kind = read.kind(arg_value)
        if kind == "segment":
            seg_type = seg_types[find.attribute(arg_value, "type")]
            if seg_type == "string_segment":
                length = get.string_segment_length(arg_value)
            elif seg_type == "list_segment":
                length = get.list_segment_length(arg_value)
            else:
                raise LowerCommandError(f"Получение длины командой Len для "
                                        f"типа {arg_type} не определено")
            num = append.data_segment("number", length)
            append.memory_stack("link", num)
        else:
            raise LowerCommandError(f"Получение длины командой Len для "
                                    f"типа {arg_type} не определено")
    else:
        raise LowerCommandError(f"Поведение команды Len с аргументом типа"
                                f"{arg_type} не определено")
