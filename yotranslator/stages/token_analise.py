from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.classes.yo_object import YoObject
from yotranslator.functions.is_object import is_object


def token_analise(token, result, coords):
    """смысловой анализ токена"""
    group, sub_group, color_group = "", "", ""
    pre_token = result[-1]
    if token.startswith(space) or token == empty:
        group = "indent"
        sub_group = "indent"
        color_group = "non colored"
    elif token in groups["math"]:
        group = "math"
        if token == "-":
            if is_object(pre_token):
                sub_group = "-"
            else:
                sub_group = "~"
        color_group = "sign"
    elif token in groups["comparison"]:
        group = "comparison"
        color_group = "sign"
    elif token in groups["logic"]:
        group = "logic"
        color_group = "sign"
    elif token in groups["structure_words"]:
        group = "structure_word"
        color_group = "structure"
    elif token in groups["interrupt_words"]:
        group = "interrupt"
        color_group = "structure"
    elif token == "=":
        group = "equating"
        color_group = "sign"
    elif token == "[":
        if is_object(pre_token):
            group = "sub_object"
        else:
            group = "object"
            sub_group = "list"
        color_group = "sign"
    elif token == "(":
        if is_object(pre_token):
            group = "call"
        else:
            group = "expression"
        color_group = "sign"
    elif token == "{":
        group = "program"
        sub_group = "scopes_program"
        color_group = "sign"
    elif token == ":":
        group = "program"
        sub_group = "oneline_program"
        color_group = "sign"
    elif token in groups["punctuation"]:
        group = "punctuation"
        color_group = "sign"
    elif token[0] in quotes:
        group = "object"
        sub_group = "string"
        color_group = "string"
        token = token[1:-1]  # обрезка кавычек
    elif token.isdigit():
        group = "object"
        sub_group = "number"
        color_group = "number"
    elif token in groups["logic_values"]:
        group = "object"
        sub_group = "logic"
        color_group = "logic_value"
    elif token == "none":
        group = "object"
        sub_group = "none"
        color_group = "object"
    elif token[0].isalpha():
        group = "object"
        sub_group = "name"
        color_group = "object"
    else:
        raise TokenError(f"Неизвестный токен {token}")
    if sub_group == empty:
        sub_group = token
    func = {"group": group, "sub_group": sub_group, "name": token,
            "color_group": color_group}
    obj = YoObject(pre_token, func, coords)
    if obj.group != "indent":
        obj.set_indent(result[-1].indent)
    else:
        obj.set_indent(len(obj.name))
    return obj
