from yovirmac.modules.errors import *
from yovirmac.modules.object_control import link
from yovirmac.modules.tape_control import append


def Negative(arg):
    obj_type, value = link.get(arg)
    if obj_type == "number":
        value = -value
        num = append.data_segment(obj_type, value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типа {obj_type} не определена операция "
                                f"инверсии Neg")


def Add(left, right):
    left_type, left_value = link.get(left)
    right_type, right_value = link.get(right)
    if left_type == "number" and right_type == "number":
        value = left_value + right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типов {left_type} и {right_type} операция"
                                f"сложения Add не определена")


def Increment(arg):
    obj_type, value = link.get(arg)
    if obj_type == "number":
        value += 1
        num = append.data_segment(obj_type, value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типа {obj_type} не определена операция "
                                f"инкремента Inc")


def Decrement(arg):
    obj_type, value = link.get(arg)
    if obj_type == "number":
        value -= 1
        num = append.data_segment(obj_type, value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типа {obj_type} не определена операция "
                                f"инверсии Dec")


def Subtract(left, right):
    left_type, left_value = link.get(left)
    right_type, right_value = link.get(right)
    if left_type == "number" and right_type == "number":
        value = left_value - right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типов {left_type} и {right_type} операция"
                                f"вычитания Sub не определена")


def Multiply(left, right):
    left_type, left_value = link.get(left)
    right_type, right_value = link.get(right)
    if left_type == "number" and right_type == "number":
        value = left_value * right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типов {left_type} и {right_type} операция"
                                f"умножения Mul не определена")


def Divide(left, right):
    left_type, left_value = link.get(left)
    right_type, right_value = link.get(right)
    if left_type == "number" and right_type == "number":
        if right_value == 0:
            raise LowerCommandError("Результат деления на ноль не определён")
        value = int(left_value / right_value)
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типов {left_type} и {right_type} операция"
                                f"деления Div не определена")


def Modulo(left, right):
    left_type, left_value = link.get(left)
    right_type, right_value = link.get(right)
    if left_type == "number" and right_type == "number":
        if right_value == 0:
            raise LowerCommandError("Результат остатка деления на ноль не "
                                    "определён")
        value = left_value % right_value
        num = append.data_segment("number", value)
        append.memory_stack("link", num)
    else:
        raise LowerCommandError(f"Для типов {left_type} и {right_type} операция"
                                f"остаток от деления Mod не определена")
