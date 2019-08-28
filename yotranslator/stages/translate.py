from yotranslator.modules.errors import *
from yotranslator.modules.constants import *
from yotranslator.stages.token_analise import token_analise
from yotranslator.stages.syntax_analise import syntax_analise
from yotranslator.classes.yo_object import YoObject
from yotransliteration import transliterator
import yotranslator.functions.highlight as highlight


def translate(program, language):
    """обработка символов и превращение их в слова"""
    program += "\n\n"
    pre_symbol, word, pre_group, quote = "\n", "", "line feed", ""
    result = []
    stores = []
    result += [YoObject(None, {"group": "program",
                               "sub_group": "indent_program",
                               "name": "program",
                               "color_group": "non colored"},
                        [0, 0])]
    result[0].set_indent(0)
    stores = [result[0]]
    row, col = 0, 0

    for symbol in program:
        if pre_symbol == "\n" and symbol != space:
            word, result, stores = add_indent(result, stores)
        if symbol == comment:
            if pre_group != "comment":
                if quote == empty:
                    word, result, stores = add_word(word, result, stores,
                                                    [row, col], language)
                    pre_group = "comment"
                else:
                    word += symbol
        elif symbol in ["\n", "\r"]:
            if pre_group != "line feed":
                if word:
                    word, result, stores = add_word(word, result, stores,
                                                    [row, col], language)
                    word += symbol
                pre_group = "line feed"
            row += 1
            col = -1
        elif pre_group == "comment":
            pass
        elif symbol in quotes:
            if quote == empty:
                word, result, stores = add_word(word, result, stores,
                                                [row, col], language)
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
                    word, result, stores = add_word(word, result, stores,
                                                    [row, col], language)
                word += symbol
            elif pre_group != "space":
                word, result, stores = add_word(word, result, stores,
                                                [row, col], language)
                pre_group = "space"
            else:
                pass
        elif symbol in signs:
            if not (pre_group == "sign" and word + symbol in sign_combos):
                word, result, stores = add_word(word, result, stores,
                                                [row, col], language)
            pre_group = "sign"
            word += symbol
        elif symbol.isalpha():
            if pre_group in ["sign", "line feed"]:
                word, result, stores = add_word(word, result, stores,
                                                [row, col], language)
            pre_group = "alpha"
            word += symbol
        elif symbol.isdigit():
            if pre_group in ["sign", "line feed"]:
                word, result, stores = add_word(word, result, stores,
                                                [row, col], language)
            pre_group = "digit"
            word += symbol
        else:
            raise TokenError(f"Неизвестный символ \"{symbol}\"")
        pre_symbol = symbol
        col += 1
    word, result, stores = add_word(word, result, stores,
                                    [row, col], language)

    if stores[0].args:
        result = stores[0].args[-1].check_close(result)
    stores[0].set_close(result)
    result = stores[0].check_close(result)
    stores = stores[:-1]

    return result


def add_word(word, result, stores, coords, language):
    """добавление токена к программе"""
    if word != empty:
        word = transliterator.transliterate(word, lang_current=language, lang_need="en")
        obj = token_analise(word, result, coords)
        highlight.add_token(obj)
        result, stores = syntax_analise(obj, result, stores)
    return "", result, stores


def add_indent(result, stores):
    """добавление отступа"""
    obj = token_analise("", result, [0, 0])
    result, stores = syntax_analise(obj, result, stores)
    return "\n", result, stores
