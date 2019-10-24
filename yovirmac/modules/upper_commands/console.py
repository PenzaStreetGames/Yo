from yovirmac.modules.constants import *
from yovirmac.modules.errors import *
from yovirmac.modules.tape_control import make, append, get
from yovirmac.modules.object_control import link, draw, to_string
from PyQt5.QtWidgets import QInputDialog
import yovirmac.modules.constants as constants


def Input():
    global input_data
    if constants.mode == "console":
        value = input()
    elif constants.mode == "editor":
        string, press = QInputDialog.getText(editor, "Ввод",
                                             "Программа запрашивает ввод")
        value = string if press else ""
        constants.input_data = constants.input_data + [value]
    else:
        raise UndefinedBehaviour(f"Неопределённое поведение команды ввода "
                                 f"для режима {constants.mode}")
    num = make.string_segment(value)
    append.memory_stack("link", num)


def Output(arg):
    arg_type, arg_value = arg
    if arg_type == "link":
        value_type, value = get.entity(arg_value)
        if value_type == "link":
            arg_value = value
            value_type, value = get.entity(value)
        if constants.mode == "console":
            draw.entity(arg_value)
        elif constants.mode == "editor":
            if value_type == "none":
                value = "none"
            constants.output_data = constants.output_data + [to_string.entity(arg_value)]
        append.memory_stack("link", 0)
    else:
        raise UndefinedBehaviour(f"Поведение команды Out с аргументом типа"
                                 f"{arg_type} не определено")
