key_words = ["while", "if", "else", "break", "continue", "none", "true",
             "false", "not", "and", "or", "xor"]
functions = ["print", "input", "len"]
signs = ["=", "[", "]", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/",
         "%", "|", ">", "<", "?"]
sign_combos = ["=?"]
quotes = ["'", '"']
comment = "#"
space, empty = " ", ""
stores = []

groups = {
    "punctuation": [",", ";", "\n", "{", "}", ":", ")", "]"],
    "math": ["+", "-", "*", "/", "%"],
    "comparison": [">", "=?", "<"],
    "logic": ["not", "and", "or", "xor"],
    "equating": ["="],
    "structure_words": ["if", "else", "while", "break", "continue"],
    "logic_values": ["true", "false"]
}

group_priority = {
    "object": 1,
    "expression": 2,
    "sub_object": 3,
    "call": 4,
    "math": 5,
    "comparison": 6,
    "logic": 7,
    "equating": 8,
    "punctuation": 9,
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
    "expression":
    {
        "(": 1
    },
    "sub_object":
    {
        "[": 1
    },
    "call":
    {
        "(": 1
    },
    "math":
    {
        "+": 3,
        "-": 3,
        "*": 2,
        "/": 2,
        "%": 2,
        "~": 1
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
    "punctuation":
    {
        ",": 1,
        ";": 1,
        ":": 1,
        ")": 1,
        "]": 1,
        "{": 1,
        "}": 1,
        "\n": 1
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
    "expression":
    {
        "(": "many"
    },
    "sub_object":
    {
        "[": "binary"
    },
    "call":
    {
        "(": "binary"
    },
    "math":
    {
        "+": "binary",
        "-": "binary",
        "*": "binary",
        "/": "binary",
        "%": "binary"
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
    "punctuation":
    {
        ",": 1,
        ";": 1,
        ":": 1,
        ")": 1,
        "]": 1,
        "{": 1,
        "}": 1,
        "\n": 1
    },
    "key_word":
    {
        "while": 1,
        "if": 1
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

    def __init__(self, parent, func):
        self.parent = parent
        self.func = func
        self.args = []
        self.priority = [group_priority[func["group"]],
                         priority[func["group"]][func["sub_group"]]]
        self.name = func["name"]
        self.sub_group = func["sub_group"]
        self.group = func["group"]
        self.args_number = args_number[self.group][self.sub_group]
        self.commas, self.points = get_punctuation(self)
        self.close = False
        self.indent = 0
        self.indent_depend = True

    def check_close(self, result):
        if self.args_number == "no":
            pass
        elif self.args_number == "unary":
            if len(self.args) != 1:
                raise YoSyntaxError(f"Неправильное число аргументов {self}")
        elif self.args_number == "binary" or self.args_number == "binary_right":
            if len(self.args) != 2:
                raise YoSyntaxError(f"Неправильное число аргументов {self}")
        elif self.args_number == "many":
            if not self.close:
                raise YoSyntaxError("Незакрытое перечисление")
        for arg in self.args:
            result = arg.check_close(result)
            result = arg.set_close(result).copy()
        return result
    
    def set_close(self, result):
        self.close = True
        if result[-1] == self:
            result = result[:-1]
        return result

    def add_arg(self, yo_object):
        self.args += [yo_object]
        yo_object.parent = self

    def remove_arg(self):
        yo_object = self.args.pop()
        return yo_object

    def __str__(self):
        if self.sub_group == self.name:
            return f"{self.group} \"{self.name}\""
        else:
            return f"{self.sub_group} \"{self.name}\""

    def __repr__(self):
        if self.sub_group == self.name:
            return f"{self.group} \"{self.name}\" {self.args}"
        else:
            return f"{self.sub_group} \"{self.name}\" {self.args}"


def translate(program):
    # token_split
    global stores
    pre_symbol, word, pre_group, quote = "", "", "", ""
    result = []
    result += [YoObject(None, {"group": "program", "sub_group": "program",
                               "name": "program"})]
    stores = [result[0]]

    for symbol in program:
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
    word, result = add_word(word, result)

    result[0].set_close(result)
    result[0].check_close(result)

    return result


def add_word(word, result):
    global stores
    if word != empty:
        obj = token_analise(word, result)
        result, stores = syntax_analise(obj, result, stores)
    return "", result


def token_analise(token, result):
    group, sub_group = "", ""

    pre_token = result[-1]
    if token.startswith(space):
        group = "indent"
        sub_group = "indent"
    elif token in groups["math"]:
        group = "math"
        if token == "-":
            if is_object(pre_token, result):
                sub_group = "-"
            else:
                sub_group = "~"
    elif token in groups["comparison"]:
        group = "comparison"
    elif token in groups["logic"]:
        group = "logic"
    elif token in groups["structure_words"]:
        group = "key_word"
    elif token in groups["punctuation"]:
        group = "punctuation"
    elif token == "=":
        group = "equating"
    elif token == "[":
        if is_object(pre_token, result):
            group = "sub_object"
        else:
            group = "object"
            sub_group = "list"
    elif token == "(":
        if is_object(pre_token, result):
            group = "call"
        else:
            group = "expression"
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

    return obj


def get_punctuation(yo_object):
    if yo_object.group == "program":
        return [";", "\n"], ["}"]
    elif yo_object.group == "key_word":
        return [":", "{"], ["}"]
    elif yo_object.group == "list":
        return [","], ["]"]
    elif yo_object.group == "call":
        return [","], [")"]
    elif yo_object.group == "expression":
        return [], [")"]
    elif yo_object.group == "sub_object":
        return [], ["]"]
    else:
        return [], []


def syntax_analise(yo_object, result, stores):
    pre_object = result[-1]
    last_store = stores[-1]
    yo_object.indent = pre_object.indent
    if yo_object.name in last_store.commas:
        result = last_store.args[-1].check_close(result)
        result.pop()
    elif yo_object.name in last_store.points:
        result = last_store.args[-1].check_close(result)
        last_store.set_close()
        stores = stores[:-1]
    elif yo_object in groups["punctuation"]:
        raise YoSyntaxError("Недопустимый в данном месте знак пунктуации")
    elif yo_object.group == "indent":
        yo_object.indent = len(yo_object.name)
    elif pre_object.args_number == "no":
        if yo_object.args_number == "binary":
            pre_object.parent.remove_arg()
            pre_object.parent.add_arg(yo_object)
            yo_object.add_arg(pre_object)
            result[-1] = yo_object
        else:
            raise YoSyntaxError("Неразделённые объекты")
    elif pre_object.args_number == "unary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError("Неразделённые объекты")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError("Неразделённые объекты")
        elif yo_object.args_number == "binary":
            if len(pre_object.args) == 1:
                pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError("Неразделённые объекты")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError("Неразделённые объекты")
    elif pre_object.args_number == "binary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError("Неразделённые объекты")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError("Неразделённые объекты")
        elif yo_object.args_number == "binary":
            if len(pre_object.args) == 2:
                priority = ""
                left = pre_object.priority.copy()
                right = yo_object.priority.copy()
                if left[0] != right[0]:
                    priority = "left" if left[0] >= right[0] else "right"
                else:
                    priority = "left" if left[1] >= right[1] else "right"
                if priority == "left":
                    arg2 = pre_object.remove_arg()
                    yo_object.add_arg(arg2)
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                elif priority == "right":
                    pre_object.parent.remove_arg()
                    pre_object.parent.add_arg(yo_object)
                    yo_object.add_arg(pre_object)
                    result[-1] = yo_object
            else:
                raise YoSyntaxError("Неразделённые объекты")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError("Неразделённые объекты")
    elif pre_object.args_number == "many":
        if pre_object.close:
            if yo_object.args_number == "binary":
                pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError("Неразделённые объекты")
        else:
            if len(pre_object.args) == 0:
                if yo_object.args_number in ["no", "unary"]:
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                elif yo_object.args_number == "many":
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                    stores += [yo_object]
                elif yo_object.args_number == "many":
                    raise YoSyntaxError("Неразделённые объекты")
            else:
                raise YoSyntaxError("Неразделённые объекты")
    else:
        raise YoSyntaxError("Неизвестный объект")
    return result, stores


def is_object(token, result):
    return token.check_close(result) and token.group in ["sub_object", "call",
                                                         "object", "expression"]


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    print(result)