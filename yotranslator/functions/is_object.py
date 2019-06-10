from yotranslator.modules.errors import *


def is_object(token):
    """является ли токен объектом"""
    objects = ["sub_object", "call", "object", "expression"]
    if token.args_number == "no":
        if token.group in objects:
            return True
        return False
    elif token.args_number == "unary":
        if len(token.args) == 1:
            child = token.args[0]
            if child.group in objects:
                return True
            return False
        return False
    elif token.args_number == "binary":
        if len(token.args) == 2:
            child = token.args[1]
            if child.group in objects:
                return True
            return False
        return False
    elif token.args_number == "many":
        if token.is_close() and token.group in objects:
            return True
        return False
    raise YoSyntaxError(f"Неизвестный объект {token}")
