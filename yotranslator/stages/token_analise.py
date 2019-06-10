from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.classes.yo_object import YoObject
from yotranslator.functions.is_object import is_object


def token_analise(token, result):
    """смысловой анализ токена"""
    group, sub_group = "", ""
    pre_token = result[-1]
    if token.startswith(space) or token == empty:
        group = "indent"
        sub_group = "indent"
    elif token in groups["math"]:
        group = "math"
        if token == "-":
            if is_object(pre_token):
                sub_group = "-"
            else:
                sub_group = "~"
    elif token in groups["comparison"]:
        group = "comparison"
    elif token in groups["logic"]:
        group = "logic"
    elif token in groups["structure_words"]:
        group = "structure_word"
    elif token in groups["interrupt_words"]:
        group = "interrupt"
    elif token == "=":
        group = "equating"
    elif token == "[":
        if is_object(pre_token):
            group = "sub_object"
        else:
            group = "object"
            sub_group = "list"
    elif token == "(":
        if is_object(pre_token):
            group = "call"
        else:
            group = "expression"
    elif token == "{":
        group = "program"
        sub_group = "scopes_program"
    elif token == ":":
        group = "program"
        sub_group = "oneline_program"
    elif token in groups["punctuation"]:
        group = "punctuation"
    elif token[0] in quotes:
        group = "object"
        sub_group = "string"
    elif token.isdigit():
        group = "object"
        sub_group = "number"
    elif token in groups["logic_values"]:
        group = "object"
        sub_group = "logic"
    elif token == "none":
        group = "object"
        sub_group = "none"
    elif token[0].isalpha():
        group = "object"
        sub_group = "name"
    else:
        raise TokenError(f"Неизвестный токен {token}")
    if sub_group == empty:
        sub_group = token
    func = {"group": group, "sub_group": sub_group, "name": token}
    obj = YoObject(pre_token, func)
    if obj.group != "indent":
        obj.set_indent(result[-1].indent)
    else:
        obj.set_indent(len(obj.name))
    return obj
