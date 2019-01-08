key_words = ["while", "if"]
structure_words = ["while", "if"]
functions = ["print"]
signs = ["=", "[", "]", "<", ">", ":", "+", "(", ")", ","]
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
        "number": 1,
        "list": 1
    },
    "brackets":
    {
        "(": 1,
        ")": 1,
        ",": 1
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
        "+": 5,
        "-": 5,
        "*": 4,
        "/": 4,
        "%": 4,
        "^": 3,
        "^/": 2,
        "|": 1
    },
    "comparison":
    {
        "=?": 1,
        "!=": 1,
        ">": 1,
        "<": 1,
        ">=": 1,
        "<=": 1
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
        ":": 1
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
        "number": "no",
        "list": "many"
    },
    "brackets":
    {
        "(": "many",
        ")": "no",
        ",": "no"
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
        "^": "binary",
        "^/": "binary",
        "|": "unary"
    },
    "comparison":
    {
        "=?": "binary",
        "!=": "binary",
        ">": "binary",
        "<": "binary",
        ">=": "binary",
        "<=": "binary"
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
        ":": "no"
    },
    "key_word":
    {
        "while": "binary_right",
        "if": "binary_right"
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


class SyntaxError(Exception):
    pass


class Object:
    def __init__(self, parent, func):
        self.parent = parent
        self.func = func
        self.args = []
        self.priority = [group_priority[func["group"]],
                         priority[func["group"]][func["sub_group"]]]
        self.name = func["name"]
        self.group = func["group"]
        self.sub_group = func["sub_group"]
        self.args_number = args_number[self.group][self.sub_group]
        self.close = False

    def __str__(self):
        if self.sub_group == self.name:
            return f"{self.group} \"{self.name}\" {self.priority}"
        else:
            return f"{self.sub_group} \"{self.name}\" {self.priority}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, y):
        return self.priority == y.priority

    def __gt__(self, y):
        if self.priority[0] != y.priority[0]:
            return priority[0] > y.priority[0]
        else:
            return priority[1] > y.priority[1]

    def __lt__(self, y):
        if self.priority[0] != y.priority[0]:
            return priority[0] < y.priority[0]
        else:
            return priority[1] < y.priority[1]


def translate(program):
    word, result = "", []

    def add_word(word, result):
        if word != empty:
            token = token_analise(word, result)
            result = context_analise(token, result)
        word = ""
        return word, result

    pre_symbol = ""
    for symbol in program:
        if symbol == "\n" or symbol == "\r":
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


def token_analise(token, tokens):
    group = ""
    sub_group = ""
    if tokens:
        pre_group = tokens[-1].func["group"]
    else:
        pre_group = ""
    if token.startswith(special_symbols["indent"]):
        group = "indent"
    elif token.isdigit():
        group = "object"
        sub_group = "number"
    elif token in signs:
        if token == "+":
            group = "math"
        elif token == "=":
            group = "equating"
        elif token == ">":
            group = "comparison"
        elif token == "<":
            group = "comparison"
        elif token == ":":
            group = "structure"
        elif token == "[":
            if pre_group != "object":
                group = "object"
                sub_group = "list"
            else:
                group = "sub_object"
        elif token == "]":
            group = "object"
            sub_group = "list"
        elif token == "(":
            if pre_group != "object":
                group = "brackets"
            else:
                group = "call"
        elif token == ")":
            group = "brackets"
        elif token == ",":
            group = "brackets"
    elif token in key_words:
        group = "key_word"
    elif token[0].isalpha():
        group = "object"
        sub_group = "name"
    else:
        raise TokenError(f"Неизвестный токен {token}")
    if sub_group == empty:
        sub_group = token
    token = {"name": token, "group": group, "sub_group": sub_group}
    obj = Object(None, token)
    return obj


def context_analise(token, tokens):
    if not tokens:
        if token.args_number == "binary":
            raise SyntaxError(f"Слева от {token.name} ничего нет")
        return [token]
    pre_token = tokens[-1]
    # дописать
    tokens += [token]

    return tokens


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        objects = []
        result = translate(infile.read())
    print(result)
