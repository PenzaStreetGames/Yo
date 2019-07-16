from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append, get


def Negative(arg):
    arg_type, obj_type, value = link.unpack(arg)
    if obj_type == "number":
        value = -value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типа {obj_type} не определена операция "
                                 f"инверсии Neg")


def Add(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        value = left_value + right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция сложения Add не определена")


def Increment(arg):
    arg_type, obj_type, value = link.unpack(arg)
    if obj_type == "number":
        value += 1
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типа {obj_type} не определена операция "
                                 f"инкремента Inc")


def Decrement(arg):
    arg_type, obj_type, value = link.unpack(arg)
    if obj_type == "number":
        value -= 1
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типа {obj_type} не определена операция "
                                 f"инверсии Dec")


def Subtract(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        value = left_value - right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция вычитания Sub не определена")


def Multiply(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        value = left_value * right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция умножения Mul не определена")


def Divide(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        if right_value == 0:
            raise UndefinedBehaviour("Результат деления на ноль не определён")
        value = int(left_value / right_value)
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(f"Для типов {left_type} и {right_type} "
                                 f"операция деления Div не определена")


def Modulo(left, right):
    left_arg_type, left_type, left_value = link.unpack(left)
    right_arg_type, right_type, right_value = link.unpack(right)
    if left_type == "number" and right_type == "number":
        if right_value == 0:
            raise UndefinedBehaviour("Результат остатка деления на ноль не "
                                     "определён")
        value = left_value % right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise UndefinedBehaviour(
            f"Для типов {left_type} и {right_type} операция остаток от деления "
            f"Mod не определена")
