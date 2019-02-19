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
argument_words = ["while", "if", "else if"]

groups = {
    "punctuation": [",", ";", "\n", "}", ":", ")", "]"],
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
    "structure_word": 10,
    "indent": 15,
    "program": 20
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
            "(": 1,
            "call_expression": 1,
            "index_expression": 1
        },
    "sub_object":
        {
            "[": 1,
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
    "structure_word":
        {
            "while": 1,
            "if": 1,
            "else": 1
        },
    "indent":
        {
            "indent": 1
        },
    "program":
        {
            "indent_program": 1,
            "scopes_program": 1,
            "oneline_program": 1
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
            "(": "many",
            "index_expression": "many",
            "call_expression": "many"
        },
    "sub_object":
        {
            "[": "many"
        },
    "call":
        {
            "(": "many"
        },
    "math":
        {
            "+": "binary",
            "-": "binary",
            "*": "binary",
            "/": "binary",
            "%": "binary",
            "~": "unary"
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
            ",": "no",
            ";": "no",
            ":": "no",
            ")": "no",
            "]": "no",
            "}": "no",
            "\n": "no"
        },
    "structure_word":
        {
            "while": "many",
            "if": "many",
            "else": "many"
        },
    "indent":
        {
            "indent": "no"
        },
    "program":
        {
            "indent_program": "many",
            "scopes_program": "many",
            "oneline_program": "many"
        }
}

virtual_commands = {
    "[": "Rar",
    "(": "Cal",
    "+": "Add",
    "-": "Sub",
    "*": "Mul",
    "/": "Div",
    "%": "Mod",
    "~": "Neg",
    "=?": "Eql",
    ">": "Grt",
    "<": "Les",
    "not": "Not",
    "and": "And",
    "or": "Or",
    "xor": "Xor"
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
        self.inside_indent = 0

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

    def is_close(self):
        if self.args_number == "no":
            return len(self.args) == 0
        elif self.args_number == "unary":
            return len(self.args) == 1
        elif self.args_number == "binary":
            return len(self.args) == 2
        elif self.args_number == "many":
            return self.close

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
            result = self.group
        else:
            result = self.sub_group
        result += " " + self.name
        for arg in self.args:
            result += "\n" + "    " * self.get_nesting(1) + arg.__repr__()
        return result

    def __repr__(self):
        if self.sub_group == self.name:
            result = self.group
        else:
            result = self.sub_group
        result += " " + self.name
        for arg in self.args:
            result += "\n" + "    " * self.get_nesting(1) + arg.__repr__()
        return result

    def get_nesting(self, number):
        if self.parent is not None:
            number = self.parent.get_nesting(number + 1)
        return number


class Program:

    def __init__(self, commands):
        self.commands = commands

    def insert(self, command, place):
        self.commands.insert(command, place)

    def add(self, command):
        self.commands += [command]


class Command:

    def __init__(self, name, *arguments):
        self.name = name
        self.args = arguments


class Argument:

    def __init__(self, arg_type, value):
        self.arg_type = arg_type
        self.value = value


def translate(program):
    # token_split
    global stores
    program += "\n\n"
    pre_symbol, word, pre_group, quote = "\n", "", "line feed", ""
    result = []
    result += [YoObject(None, {"group": "program",
                               "sub_group": "indent_program",
                               "name": "program"})]
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
    global stores
    if word != empty:
        obj = token_analise(word, result)
        result, stores = syntax_analise(obj, result, stores)
    return "", result


def add_indent(result):
    global stores
    obj = token_analise("", result)
    result, stores = syntax_analise(obj, result, stores)
    return "\n", result


def token_analise(token, result):
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
        obj.indent = result[-1].indent
    else:
        obj.indent = len(obj.name)
    return obj


def get_punctuation(yo_object):
    if yo_object.sub_group == "indent_program":
        return [";", "\n"], []
    elif yo_object.sub_group == "scopes_program":
        return [";", "\n"], ["}"]
    elif yo_object.sub_group == "oneline_program":
        return [], [";", "\n"]
    elif yo_object.group == "structure_word":
        return [":", "{"], ["}"]
    elif yo_object.sub_group == "list":
        return [","], ["]"]
    elif yo_object.sub_group == "call_expression":
        return [","], [")"]
    elif yo_object.sub_group == "index_expression":
        return [], ["]"]
    elif yo_object.group == "expression":
        return [], [")"]
    else:
        return [], []


def syntax_analise(yo_object, result, stores):
    pre_object = result[-1]
    last_store = stores[-1]
    # обработка вызова индекса
    if yo_object.group == "sub_object":
        if pre_object.args_number == "no":
            parent = pre_object.parent
            child = parent.remove_arg()
            parent.add_arg(yo_object)
            yo_object.add_arg(child)
        elif pre_object.args_number in ["unary", "binary"]:
            if is_object(pre_object):
                child = pre_object.remove_arg()
                pre_object.add_arg(yo_object)
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        elif pre_object.args_number == "many":
            if is_object(pre_object):
                child = pre_object.parent.remove_arg()
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        new_object = YoObject(None, {"group": "expression",
                                     "sub_group": "index_expression",
                                     "name": "["})
        yo_object.add_arg(new_object)
        result[-1] = yo_object
        result += [new_object]
        stores += [new_object]
    # обработка вызова функции
    elif yo_object.group == "call":
        if pre_object.args_number == "no":
            parent = pre_object.parent
            child = parent.remove_arg()
            parent.add_arg(yo_object)
            yo_object.add_arg(child)
        elif pre_object.args_number in ["unary", "binary"]:
            if is_object(pre_object):
                child = pre_object.remove_arg()
                pre_object.add_arg(yo_object)
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        elif pre_object.args_number == "many":
            if is_object(pre_object):
                child = pre_object.parent.remove_arg()
                yo_object.add_arg(child)
            else:
                raise YoSyntaxError(f"Неправильный запрос индекса {pre_object} "
                                    f"{yo_object}")
        new_object = YoObject(None, {"group": "expression",
                                     "sub_group": "call_expression",
                                     "name": "("})
        yo_object.add_arg(new_object)
        result[-1] = yo_object
        result += [new_object]
        stores += [new_object]
    # пустые вызовы - тоже вызовы
    elif (pre_object.sub_group == "call_expression"
          and yo_object.name in last_store.points):
        result = pre_object.set_close(result)
        result = result[-1].set_close(result)
        stores = stores[:-1]
    # обработка структурных слов
    elif (last_store.group == "structure_word" and
          yo_object.group == "program"):
        if last_store.name in argument_words:
            result = last_store.args[-1].check_close(result)
            result = last_store.args[-1].set_close(result)
        last_store.add_arg(yo_object)
        result += [yo_object]
        stores += [yo_object]
    # если в однострочной структуре встречается перенос строки -
    # это отступозависимая структура
    elif (last_store.sub_group == "oneline_program" and yo_object.name == "\n"
          and len(last_store.args) == 0):
        parent = last_store.parent
        new_object = YoObject(None, {"group": "program",
                                     "sub_group": "indent_program",
                                     "name": ":"})
        last_store.parent.remove_arg()
        parent.add_arg(new_object)
        result[-1] = new_object
        stores[-1] = new_object
    # если после else идёт if, то это одна конструкция else if
    elif (last_store.group == "structure_word" and pre_object.name == "else"
          and yo_object.name == "if"):
        pre_object.name += " if"
        pre_object.sub_group += " if"
    # переносы строк после открывающейся скобки до первого слова не считаются
    elif (yo_object.name == "\n" and last_store.group == "program" and
          len(last_store.args) == 0):
        pass
    # переносы между условием структуры и телом не считаются
    elif (yo_object.name == "\n" and last_store.group == "structure_word" and
          len(last_store.args) == 1):
        pass
    elif yo_object.name in last_store.commas:
        result = last_store.args[-1].check_close(result)
        # if result[-1] != last_store:
        result = last_store.args[-1].set_close(result)
    elif yo_object.name in last_store.points:
        result = last_store.args[-1].check_close(result)
        result = last_store.args[-1].set_close(result)
        result = last_store.set_close(result)
        stores = stores[:-1]
        if result[-1].group == "sub_object":
            result[-1].close = True
        elif result[-1].group == "call":
            result[-1].close = True
        elif result[-1].group == "structure_word" and yo_object.name == "}":
            result = result[-1].set_close(result)
            stores = stores[:-1]
    elif yo_object.name in groups["punctuation"]:
        raise YoSyntaxError(f"Недопустимый в данном месте знак пунктуации "
                            f"{yo_object}")
    elif yo_object.group == "indent":
        if last_store.sub_group == "indent_program":
            if len(last_store.args) == 0:
                last_store.inside_indent = yo_object.indent
            else:
                while yo_object.indent != last_store.inside_indent:
                    if yo_object.indent < last_store.inside_indent:
                        result = last_store.args[-1].check_close(result)
                        result = last_store.args[-1].set_close(result)
                        result = last_store.set_close(result)
                        stores = stores[:-1]
                        result = result[-1].set_close(result)
                        stores = stores[:-1]
                    elif yo_object.indent > last_store.inside_indent:
                        raise YoSyntaxError(f"Неуместный отступ {pre_object}")
                    last_store = stores[-1]
    elif pre_object.args_number == "no":
        if yo_object.args_number == "binary":
            pre_object.parent.remove_arg()
            pre_object.parent.add_arg(yo_object)
            yo_object.add_arg(pre_object)
            result[-1] = yo_object
        else:
            raise YoSyntaxError(f"Неразделённые объекты "
                                f"{pre_object} {yo_object}")
    elif pre_object.args_number == "unary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        elif yo_object.args_number == "binary":
            if len(pre_object.args) == 1:
                pre_object = pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
    elif pre_object.args_number == "binary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
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
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
    elif pre_object.args_number == "many":
        if pre_object.close:
            if yo_object.args_number == "binary":
                pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
        else:
            if not last_store.close:
                if yo_object.args_number in ["no", "unary"]:
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                elif yo_object.args_number == "many":
                    pre_object.add_arg(yo_object)
                    result += [yo_object]
                    stores += [yo_object]
                elif yo_object.args_number == "many":
                    raise YoSyntaxError(f"Неразделённые объекты "
                                        f"{pre_object} {yo_object}")
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object} {yo_object}")
    else:
        raise YoSyntaxError(f"Неизвестный объект {yo_object}")
    return result, stores


def is_object(token):
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


def get_vir_commands(yo_object):
    global virtual_commands
    commands = []
    if yo_object.group == "object":
        if yo_object.sub_group == "name":
            commands = [Command("Crt", Argument("str", yo_object.name)),
                        Command("Pop", Argument("lnk", "^a")),
                        Command("Fnd", Argument("lnk", "*a"))]
        elif yo_object.sub_group == "none":
            commands = [Command("Crt", Argument("non", 0))]
        elif yo_object.sub_group == "logic":
            value = 1 if yo_object.name == "true" else 0
            commands = [Command("Crt", Argument("log", value))]
        elif yo_object.sub_group == "number":
            commands = [Command("Crt", Argument("num", int(yo_object.name)))]
        elif yo_object.sub_group == "string":
            commands = [Command("Crt", Argument("str", yo_object.name))]
        elif yo_object.sub_group == "list":
            end_command_args = []
            for i in range(len(yo_object.args)):
                argument = yo_object.args[i]
                commands += [get_vir_commands(argument)]
                commands += [Command("Pop", Argument("lnk", f"^{i}"))]
                end_command_args += [Argument("lnk", f"*{i}")]
            commands += [Command("Crt", *end_command_args)]
    elif yo_object.group == "expression":
        if yo_object.sub_group == "(":
            commands += [get_vir_commands(yo_object.args[0])]
        elif yo_object.sub_group == "call_expression":
            for child in yo_object.args:
                commands += [get_vir_commands(child)]
        elif yo_object.sub_group == "index_expression":
            commands += [get_vir_commands(yo_object.args[0])]
    elif yo_object.group == "sub_object":
        commands += [get_vir_commands(yo_object.args[1]),
                     get_vir_commands(yo_object.args[2])]
        commands += [Command("Pop", Argument("lnk", "^a")),
                     Command("Pop", Argument("lnk", "^b")),
                     Command("Rar", Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "call":
        func_name = yo_object.args[0]
        func_args = yo_object.args[1].args
        length = len(func_args)
        if func_name == "print":
            if length == 1:
                commands += [get_vir_commands(yo_object.args[1]),
                             Command("Pop", Argument("lnk", "^a")),
                             Command("Out", Argument("lnk", "*a"))]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        elif func_name == "input":
            if length == 0:
                commands += [Command("Inp")]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        elif func_name == "len":
            if length == 1:
                commands += [get_vir_commands(yo_object.args[1]),
                             Command("Pop", Argument("lnk", "^a")),
                             Command("Len", Argument("lnk", "*a"))]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        else:
            raise YoSyntaxError(f"Функции не поддерживаются, кроме print,"
                                f"len и input")
    elif yo_object.group == "math":
        for child in yo_object.args:
            commands += [get_vir_commands(child)]
        func = virtual_commands[yo_object.sub_group]
        if func != "Neg":
            commands += [Command("Pop", Argument("lnk", "^b")),
                         Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"),
                                 Argument("lnk", "*b"))]
        else:
            commands += [Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"))]
    elif yo_object.group == "comparison":
        for child in yo_object.args:
            commands += [get_vir_commands(child)]
        func = virtual_commands[yo_object.sub_group]
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command(func, Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "logic":
        for child in yo_object.args:
            commands += [get_vir_commands(child)]
        func = virtual_commands[yo_object.sub_group]
        if func != "Not":
            commands += [Command("Pop", Argument("lnk", "^b")),
                         Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"),
                                 Argument("lnk", "*b"))]
        else:
            commands += [Command("Pop", Argument("lnk", "^a")),
                         Command(func, Argument("lnk", "*a"))]
    elif yo_object.group == "equating":
        for child in yo_object.args:
            commands += [get_vir_commands(child)]
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command("Eqt", Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "structure_word":
        if yo_object.sub_group in ["if", "else if"]:
            commands += [get_vir_commands(yo_object.args[0]),
                         Command("Pop", Argument("lnk", "^a")),
                         Command("Jif", Argument("lnk", "*a"),
                                 Argument("lnk", "^next")),
                         get_vir_commands(yo_object.args[1]),
                         Command("Jmp", Argument("lnk", "^end"))]
        elif yo_object.sub_group == "else":
            commands += [get_vir_commands(yo_object.args[0])]
        elif yo_object.sub_group == "while":
            commands += [get_vir_commands(yo_object.args[0]),
                         Command("Pop", Argument("lnk", "^a")),
                         Command("Jif", Argument("lnk", "*a"),
                                 Argument("lnk", "^end")),
                         get_vir_commands(yo_object.args[1]),
                         Command("Jmp", Argument("lnk", "^begin"))]
    elif yo_object.group == "program":
        pass
    return commands


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    print(result[0])
