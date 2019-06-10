from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.stages.token_analise import token_analise
from yotranslator.stages.syntax_analise import syntax_analise
from yotranslator.classes.yo_object import YoObject


def translate(program):
    """обработка символов и превращение их в слова"""
    global stores
    program += "\n\n"
    pre_symbol, word, pre_group, quote = "\n", "", "line feed", ""
    result = []
    result += [YoObject(None, {"group": "program",
                               "sub_group": "indent_program",
                               "name": "program"})]
    result[0].set_indent(0)
    stores = [result[0]]

    for symbol in program:
        if pre_symbol == "\n" and symbol != space:
            word, result = add_indent(result)
        if symbol == comment:
            if pre_group != "comment":
                if quote == empty:
                    word, result = add_word(word, result)
                    pre_group = "comment"
                else:
                    word += symbol
        elif symbol in ["\n", "\r"]:
            if pre_group != "line feed":
                if word:
                    word, result = add_word(word, result)
                    word += symbol
                pre_group = "line feed"
        elif pre_group == "comment":
            pass
        elif symbol in quotes:
            if quote == empty:
                word, result = add_word(word, result)
                quote = symbol
                pre_group = "quote"
            elif symbol == quote:
                if pre_symbol != "\\":
                    quote = ""
            word += symbol
        elif quote != empty:
            word += symbol
        elif symbol == space:
            if pre_group == "line feed":
                if pre_symbol in ["\n", "\r"]:
                    word, result = add_word(word, result)
                word += symbol
            elif pre_group != "space":
                word, result = add_word(word, result)
                pre_group = "space"
            else:
                pass
        elif symbol in signs:
            if not (pre_group == "sign" and word + symbol in sign_combos):
                word, result = add_word(word, result)
            pre_group = "sign"
            word += symbol
        elif symbol.isalpha():
            if pre_group in ["sign", "line feed"]:
                word, result = add_word(word, result)
            pre_group = "alpha"
            word += symbol
        elif symbol.isdigit():
            if pre_group in ["sign", "line feed"]:
                word, result = add_word(word, result)
            pre_group = "digit"
            word += symbol
        else:
            raise TokenError(f"Неизвестный символ \"{symbol}\"")
        pre_symbol = symbol
    word, result = add_word(word, result)

    if stores[0].args:
        result = stores[0].args[-1].check_close(result)
    stores[0].set_close(result)
    result = stores[0].check_close(result)
    stores = stores[:-1]

    return result


def add_word(word, result):
    """добавление токена к программе"""
    global stores
    if word != empty:
        obj = token_analise(word, result)
        result, stores = syntax_analise(obj, result, stores)
    return "", result


def add_indent(result):
    """добавление отступа"""
    global stores
    obj = token_analise("", result)
    result, stores = syntax_analise(obj, result, stores)
    return "\n", result
