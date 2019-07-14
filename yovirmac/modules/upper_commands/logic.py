from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append


def Not(arg):
    arg_type, obj_type, value = link.unpack(arg)
    if obj_type == "logic":
        value = not value
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типа {obj_type} не определена операция "
                                 f"логического НЕ Not")


def And(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "logic" and right_type == "logic":
        value = left_value and right_value
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция логического И And не определена")


def Or(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "logic" and right_type == "logic":
        value = left_value or right_value
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция логического ИЛИ Or не определена")


def Xor(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "logic" and right_type == "logic":
        value = left_value + right_value == 1
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция логического ЛИБО XOR не определена")
