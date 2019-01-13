key_words = ["while", "if", "else", "break", "continue"]
functions = ["print", "input", "len"]
signs = ["=", "[", "]", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/",
         "%", "|", ">", "<", "?"]
sign_combos = ["=?"]
space, empty = " ", ""
special_symbols = {"command_end": "*ce",
                   "indent": "*i",
                   "line_indent": "*i{}"}
group_priority = {
    "object": 1,
    "brackets": 2,
    "expression": 3,
    "sub_object": 4,
    "call": 5,
    "math": 6,
    "comparison": 7,
    "logic": 8,
    "equating": 9,
    "structure": 10,
    "key_word": 11,
    "indent": 99,
    "program": 100
}

priority = {
    "object":
    {
        "name": 1,
        "none": 1,
        "logic": 1,
        "number": 1,
        "string": 1,
        "list": 1
    },
    "brackets":
    {
        "(": 1,
        ")": 1,
        ",": 1
    },
    "expression":
    {
        "(": 1,
        ")": 1
    },
    "sub_object":
    {
        ".": 1,
        "[": 1,
        "]": 1
    },
    "call":
    {
        "(": 1,
        ")": 1
    },
    "math":
    {
        "+": 4,
        "-": 4,
        "*": 3,
        "/": 3,
        "%": 3,
        "~": 2,
        "|": 1
    },
    "comparison":
    {
        "=?": 1,
        ">": 1,
        "<": 1,
    },
    "logic":
    {
        "not": 1,
        "and": 2,
        "or": 3,
        "xor": 3
    },
    "equating":
    {
        "=": 1
    },
    "structure":
    {
        ":": 1,
        "{": 1,
        "}": 1
    },
    "key_word":
    {
        "while": 1,
        "if": 1
    },
    "indent":
    {
        "indent": 1
    },
    "program":
    {
        "program": 1
    }
}

args_number = {
    "object":
    {
        "name": "no",
        "none": "no",
        "logic": "no",
        "number": "no",
        "string": "no",
        "list": "many"
    },
    "brackets":
    {
        "(": "many",
        ")": "no",
        ",": "no"
    },
    "expression":
    {
        "(": "many",
        ")": "no"
    },
    "sub_object":
    {
        ".": "binary",
        "[": "binary",
        "]": "no"
    },
    "call":
    {
        "(": "binary",
        ")": "no"
    },
    "math":
    {
        "+": "binary",
        "-": "binary",
        "*": "binary",
        "/": "binary",
        "%": "binary",
        "|": "unary"
    },
    "comparison":
    {
        "=?": "binary",
        ">": "binary",
        "<": "binary"
    },
    "logic":
    {
        "not": "unary",
        "and": "binary",
        "or": "binary",
        "xor": "binary"
    },
    "equating":
    {
        "=": "binary"
    },
    "structure":
    {
        ":": "no",
        "{": "many",
        "}": "no"
    },
    "key_word":
    {
        "while": "binary_right",
        "if": "binary_right",
        "else": "unary"
    },
    "indent":
    {
        "indent": "no"
    },
    "program":
    {
        "program": "many"
    }
}


class TokenError(Exception):
    pass


class YoSyntaxError(Exception):
    pass


class YoObject:
    pass


def translate(program):
    pre_symbol, word, quote = "", "", ""
    result = []

    def add_word(word, result):
        if word != empty:
            result += [word]
        word = ""
        return word, result

    for symbol in program:
        if quote != empty:
            word += symbol
            if symbol != quote and pre_symbol != "backslash":
                quote = ""
                word, result = add_word(word, result)
                pre_symbol = "sign"
        elif symbol == "\n" or symbol == "\r":
            if word != special_symbols["command_end"]:
                word, result = add_word(word, result)
                pre_symbol = "sign"
                # word = special_symbols["command_end"]
        elif symbol == space:
            if word == special_symbols["command_end"]:
                word, result = add_word(word, result)
                word = special_symbols["indent"]
                pre_symbol = "sign"
            elif word == special_symbols["indent"]:
                word, result = add_word(word, result)
                word = special_symbols["indent"]
                pre_symbol = "sign"
            elif pre_symbol != space:
                word, result = add_word(word, result)
                pre_symbol = "space"
            else:
                pass
        elif symbol in signs:
            if not(pre_symbol == "sign" and word + symbol in sign_combos):
                word, result = add_word(word, result)
            pre_symbol = "sign"
            word += symbol
        elif symbol.isalpha():
            if pre_symbol == "sign":
                word, result = add_word(word, result)
            pre_symbol = "alpha"
            word += symbol
        elif symbol.isdigit():
            if pre_symbol == "sign":
                word, result = add_word(word, result)
            pre_symbol = "digit"
            word += symbol
        else:
            raise TokenError(f"Неизвестный символ \"{symbol}\"")
    add_word(word, result)

    return result


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        objects = []
        result = translate(infile.read())
    print(result)