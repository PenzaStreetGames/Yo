key_words = ["while", "if", "else", "break", "continue", "none", "true",
             "false", "not", "and", "or", "xor"]
functions = ["print", "input", "len"]
signs = ["=", "[", "]", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/",
         "%", "|", ">", "<", "?"]
sign_combos = ["=?"]
quotes = ["'", '"']
comment = "#"
space, empty = " ", ""
special_symbols = {"command_end": "*ce",
                   "indent": "*i",
                   "line_indent": "*i{}"}
group_priority = {
    "object": 1,
    "brackets": 2,
    "sub_object": 3,
    "call": 4,
    "math": 5,
    "comparison": 6,
    "logic": 7,
    "equating": 8,
    "structure": 9,
    "key_word": 10,
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
        ")": 1,
        ",": 1
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
    # token_split
    pre_symbol, word, pre_group, quote = "", "", "", ""
    result = []

    def add_word(word, result):
        if word != empty:
            result += [word]
        return "", result

    for symbol in program:
        if symbol == comment:
            if pre_group != "comment":
                if quote == empty:
                    word, result = add_word(word, result)
                    pre_group = "comment"
                else:
                    word += symbol
        elif symbol in ["\n", "\r"]:
            if pre_group != "line feed" and word:
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
                word += symbol
            elif pre_group != "space":
                word, result = add_word(word, result)
                pre_group = "space"
            else:
                pass
        elif symbol in signs:
            if not(pre_group == "sign" and word + symbol in sign_combos):
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
    add_word(word, result)

    return result


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        objects = []
        result = translate(infile.read())
    print(result)