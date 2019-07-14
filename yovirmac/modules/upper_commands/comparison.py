from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append


def Equal(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        value = left_value == right_value
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция сравнения Eql не определена")


def Great(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        value = left_value > right_value
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция больше Grt не определена")


def Less(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        value = left_value < right_value
        num = append.data_segment("logic", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция меньше Less не определена")
