key_words = ["while", "if", "else", "elseif", "break", "continue", "none",
             "true", "false", "not", "and", "or", "xor"]
functions = ["print", "input", "len"]
signs = ["=", "[", "]", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/",
         "%", "|", ">", "<", "?"]
sign_combos = ["=?"]
quotes = ["'", '"']
comment = "#"
space, empty = " ", ""
stores = []
argument_words = ["while", "if", "elseif"]
branching_words = ["if", "elseif", "else"]
branching_continue_words = ["elseif", "else"]
# группы ключевых слов
groups = {
    "punctuation": [",", ";", "\n", "}", ":", ")", "]"],
    "math": ["+", "-", "*", "/", "%"],
    "comparison": [">", "=?", "<"],
    "logic": ["not", "and", "or", "xor"],
    "equating": ["="],
    "structure_words": ["if", "else", "elseif", "while"],
    "logic_values": ["true", "false"],
    "interrupt_words": ["break", "continue"],
}
# приоритет групп токенов
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
    "interrupt": 10,
    "structure_word": 11,
    "indent": 15,
    "program": 20
}
# приоритет конкретных токенов в группе
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
            "index_expression": 1,
            "branching": 1
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
    "interrupt":
        {
            "break": 1,
            "continue": 1
        },
    "structure_word":
        {
            "while": 1,
            "if": 1,
            "else": 1,
            "elseif": 1
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
# число аргументов у токена
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
            "call_expression": "many",
            "branching": "many"
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
    "interrupt":
        {
            "break": "no",
            "continue": "no"
        },
    "structure_word":
        {
            "while": "many",
            "if": "many",
            "else": "many",
            "elseif": "many"
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
# соответствие токенов и виртуальных команд
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
# байтовая длина системных типов
vir_args_size = {
    "non": 1,
    "lnk": 1,
    "log": 1,
    "num": 1,
    "str": "many",
    "lst": 1
}
# специальные ссылки
special_links = ["next_branch", "branch_begin", "branching_end",
                 "cycle_begin", "cycle_end", "rubbish"]


class TokenError(Exception):
    """Ошибка считывания токена"""
    pass


class YoSyntaxError(Exception):
    """Синтаксическая ошибка языка"""
    pass


class YoObject:
    """объект кода"""

    def __init__(self, parent, func):
        """инициализация объекта"""
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
        """проверка на возможность закрытия"""
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
                if self.sub_group == "branching":
                    result = self.set_close(result)
                else:
                    raise YoSyntaxError(f"Незакрытое перечисление {self}")
        for arg in self.args:
            result = arg.check_close(result)
            result = arg.set_close(result).copy()
        return result

    def is_close(self):
        """закрыт ли объект для новых аргументов"""
        if self.args_number == "no":
            return len(self.args) == 0
        elif self.args_number == "unary":
            return len(self.args) == 1
        elif self.args_number == "binary":
            return len(self.args) == 2
        elif self.args_number == "many":
            return self.close

    def set_close(self, result):
        """закрытие объекта для новых аргументов"""
        self.close = True
        if result[-1] == self:
            result = result[:-1]
        return result

    def add_arg(self, yo_object):
        """добавление аргумента"""
        self.args += [yo_object]
        yo_object.parent = self

    def remove_arg(self):
        """удаление аргумента"""
        yo_object = self.args.pop()
        return yo_object

    def __str__(self):
        """строковое представление объекта"""
        if self.sub_group == self.name:
            result = self.group
        else:
            result = self.sub_group
        result += " " + self.name
        for arg in self.args:
            result += "\n" + "    " * self.get_nesting(1) + arg.__repr__()
        return result

    def __repr__(self):
        """тоже представление объекта"""
        if self.sub_group == self.name:
            result = self.group
        else:
            result = self.sub_group
        result += " " + self.name
        for arg in self.args:
            result += "\n" + "    " * self.get_nesting(1) + arg.__repr__()
        return result

    def get_nesting(self, number):
        """получить уровень вложенности объекта"""
        if self.parent is not None:
            number = self.parent.get_nesting(number + 1)
        return number

    def set_indent(self, indent, inside=False):
        if not inside:
            if self.group == "structure_word":
                self.parent.set_indent(indent, inside=True)
            self.indent = indent
        else:
            self.inside_indent = indent
            if self.sub_group == "branching":
                self.indent = indent
            elif self.sub_group == "indent_program":
                self.indent = indent
        if self.sub_group == "indent_program":
            if self.parent and self.parent.group == "structure_word":
                self.parent.set_indent(indent, inside=True)
            self.indent = indent
            self.inside_indent = indent


class Program:
    """программа байтовых команд"""

    def __init__(self, commands):
        """инициализация с загрузкой команд"""
        self.commands = commands
        self.next_cell = 0

    def insert(self, command, place):
        """вставить команду в нужное место"""
        self.commands.insert(command, place)

    def add(self, command):
        """добавить команду"""
        command.set_cell(self.next_cell)
        self.commands += [command]
        self.next_cell += command.get_size()

    def __str__(self):
        return "\n".join(map(str, self.commands))

    def __repr__(self):
        return self.__str__()


class Command:
    """байтовая команда"""

    def __init__(self, name, *arguments):
        """инициализация команды"""
        self.name = name
        self.args = arguments
        self.cell = 0
        self.size = self.get_size()

    def set_cell(self, cell):
        self.cell = cell
        arg_cell = cell + 2
        for arg in self.args:
            arg.set_cell(arg_cell)
            arg_cell += arg.get_size()


    def get_size(self):
        """длина команды в ячейках"""
        length = 2
        for arg in self.args:
            length += arg.get_size() + 1
        return length

    def __str__(self):
        return f"{self.cell}  {self.name}  " \
               f"{' '.join(map(lambda arg: str(arg), self.args))}"

    def __repr__(self):
        return self.__str__()


class Argument:
    """аргумент байтовой команды"""

    def __init__(self, arg_type, value):
        """инициализация аргумента"""
        self.arg_type = arg_type
        self.value = value
        self.cell = 0

    def set_cell(self, cell):
        self.cell = cell

    def get_size(self):
        if type(vir_args_size[self.arg_type]) == int:
            return vir_args_size[self.arg_type]
        elif vir_args_size[self.arg_type] == "many":
            if self.arg_type == "str":
                # один закрывающий байт, второй для симметрии
                return len(self.value) + 2

    def __str__(self):
        return f"{self.cell} {self.arg_type} {str(self.value)}"

    def __repr__(self):
        return self.__str__()


class Mark:
    """метка байтового кода"""

    def __init__(self, name):
        """инициализация метки"""
        self.value = name
        self.cell = 0

    def set_cell(self, cell):
        self.cell = cell

    def get_size(self):
        return 0

    def __str__(self):
        return f"{self.cell} {self.name}"

    def __repr__(self):
        return self.__str__()


def translate(program):
    """обработка символов и превращение их в слова"""
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


def get_punctuation(yo_object):
    """получение знаков препинания для токена"""
    if yo_object.sub_group == "indent_program":
        return [";", "\n"], []
    elif yo_object.sub_group == "scopes_program":
        return [";", "\n"], ["}"]
    elif yo_object.sub_group == "oneline_program":
        return [], [";", "\n"]
    elif yo_object.group == "structure_word":
        return [":", "{"], ["}"]
    elif yo_object.group == "interrupt":
        return [], []
    elif yo_object.sub_group == "list":
        return [","], ["]"]
    elif yo_object.sub_group == "call_expression":
        return [","], [")"]
    elif yo_object.sub_group == "index_expression":
        return [], ["]"]
    elif yo_object.sub_group == "branching":
        return ["\n"], []
    elif yo_object.group == "expression":
        return [], [")"]
    else:
        return [], []


def syntax_analise(yo_object, result, stores):
    """смысловой анализ токена в синтаксическом дереве программы"""
    pre_object = result[-1]
    last_store = stores[-1]
    # обработка закрытия ветвления
    if (last_store.sub_group == "branching" and
            last_store.args[-1].is_close() and
            yo_object.name not in branching_continue_words and
            yo_object.name != "\n"):
        print(yo_object)
        result = last_store.check_close(result)
        result = last_store.set_close(result)
        stores = stores[:-1]
        last_store = stores[-1]
        pre_object = result[-1]
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
                raise YoSyntaxError(f"Неправильный вызов функции {pre_object} "
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
    # обработка if
    elif (yo_object.group == "structure_word" and yo_object.name == "if" and
          last_store.group == "program"):
        new_object = YoObject(None, {"group": "expression",
                                     "sub_group": "branching",
                                     "name": "branching"})
        new_object.set_indent(pre_object.inside_indent, inside=True)
        yo_object.set_indent(new_object.indent)
        new_object.add_arg(yo_object)
        last_store.add_arg(new_object)
        result += [new_object, yo_object]
        stores += [new_object, yo_object]
    # обработка elseif и else
    elif (yo_object.group == "structure_word" and
          yo_object.name in branching_continue_words):
        if (last_store.sub_group == "branching" and
                last_store.args[-1].name != "else"):
            last_store.add_arg(yo_object)
            result += [yo_object]
            stores += [yo_object]
        else:
            raise YoSyntaxError("Неправильное использование else и elseif")
    # обработка содержимого структур
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
        new_object.set_indent(parent.inside_indent)
        # new_object.indent = parent.inside_indent
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
        elif result[-1].group == "structure_word":
            if last_store.sub_group == "scopes_program":
                result = result[-1].set_close(result)
                stores = stores[:-1]
            elif last_store.sub_group == "oneline_program":
                result = result[-1].set_close(result)
                stores = stores[:-1]
    elif yo_object.name in groups["punctuation"]:
        raise YoSyntaxError(f"Недопустимый в данном месте знак пунктуации "
                            f"{yo_object}")
    elif yo_object.group == "indent":
        if last_store.sub_group == "indent_program":
            if len(last_store.args) == 0:
                last_store.set_indent(yo_object.indent, inside=True)
                # last_store.inside_indent = yo_object.indent
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
                                f"{pre_object}\n{yo_object}")
    elif pre_object.args_number == "unary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "binary":
            if len(pre_object.args) == 1:
                pre_object = pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "many":
            if len(pre_object.args) == 0:
                pre_object.add_arg(yo_object)
                result += [yo_object]
                stores += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
    elif pre_object.args_number == "binary":
        if yo_object.args_number == "no":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
        elif yo_object.args_number == "unary":
            if len(pre_object.args) == 1:
                pre_object.add_arg(yo_object)
                result += [yo_object]
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
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
                                    f"{pre_object}\n{yo_object}")
    elif pre_object.args_number == "many":
        if pre_object.close:
            if yo_object.args_number == "binary":
                pre_object.parent.remove_arg()
                pre_object.parent.add_arg(yo_object)
                yo_object.add_arg(pre_object)
                result[-1] = yo_object
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
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
                                        f"{pre_object}\n{yo_object}")
            else:
                raise YoSyntaxError(f"Неразделённые объекты "
                                    f"{pre_object}\n{yo_object}")
    else:
        raise YoSyntaxError(f"Неизвестный объект {yo_object}")
    return result, stores


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


def get_vir_commands(yo_object):
    """выдать набор байтовых команд для токена"""
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
                commands += get_vir_commands(argument)
                commands += [Command("Pop", Argument("lnk", f"^{i}"))]
                end_command_args += [Argument("lnk", f"*{i}")]
            end_command_args += [Argument("non", 0)]
            commands += [Command("Crt", Argument("lst", 0), *end_command_args)]
    elif yo_object.group == "expression":
        if yo_object.sub_group == "(":
            commands += get_vir_commands(yo_object.args[0])
        elif yo_object.sub_group == "call_expression":
            for child in yo_object.args:
                commands += get_vir_commands(child)
        elif yo_object.sub_group == "index_expression":
            commands += get_vir_commands(yo_object.args[0])
        elif yo_object.sub_group == "branching":
            for branch in yo_object.args:
                commands += [Mark("#branch_begin"),
                             *get_vir_commands(branch),
                             Command("Jmp", Argument("lnk", "^branching_end"))]
            commands += [Mark("#branching_end")]
    elif yo_object.group == "sub_object":
        commands += [*get_vir_commands(yo_object.args[0]),
                     *get_vir_commands(yo_object.args[1])]
        commands += [Command("Pop", Argument("lnk", "^a")),
                     Command("Pop", Argument("lnk", "^b")),
                     Command("Rar", Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "call":
        func_name = yo_object.args[0].name
        func_args = yo_object.args[1].args
        length = len(func_args)
        if func_name == "print":
            if length == 1:
                commands += [*get_vir_commands(yo_object.args[1]),
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
                commands += [*get_vir_commands(yo_object.args[1]),
                             Command("Pop", Argument("lnk", "^a")),
                             Command("Len", Argument("lnk", "*a"))]
            else:
                raise YoSyntaxError(f"Неправильное число аргументов {func_name}"
                                    f" {length}")
        else:
            raise YoSyntaxError(f"Функции не поддерживаются, кроме print, "
                                f"len и input, но не {func_name}")
    elif yo_object.group == "math":
        for child in yo_object.args:
            commands += get_vir_commands(child)
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
            commands += get_vir_commands(child)
        func = virtual_commands[yo_object.sub_group]
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command(func, Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "logic":
        for child in yo_object.args:
            commands += get_vir_commands(child)
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
            commands += get_vir_commands(child)
        commands += [Command("Pop", Argument("lnk", "^b")),
                     Command("Pop", Argument("lnk", "^a")),
                     Command("Eqt", Argument("lnk", "*a"),
                             Argument("lnk", "*b"))]
    elif yo_object.group == "interrupt":
        if yo_object.name == "break":
            commands += [Command("Jmp", Argument("lnk", "^cycle_end"))]
        elif yo_object.name == "continue":
            commands += [Command("Jmp", Argument("lnk", "^cycle_begin"))]
    elif yo_object.group == "structure_word":
        if yo_object.sub_group in ["if", "elseif"]:
            commands += [*get_vir_commands(yo_object.args[0]),
                         Command("Pop", Argument("lnk", "^a")),
                         Command("Jif", Argument("lnk", "*a"),
                                 Argument("lnk", "^next_branch")),
                         *get_vir_commands(yo_object.args[1])]
        elif yo_object.sub_group == "else":
            commands += [*get_vir_commands(yo_object.args[0])]
        elif yo_object.sub_group == "while":
            commands += [Mark("#cycle_begin"),
                         *get_vir_commands(yo_object.args[0]),
                         Command("Pop", Argument("lnk", "^a")),
                         Command("Jif", Argument("lnk", "*a"),
                                 Argument("lnk", "^cycle_end")),
                         *get_vir_commands(yo_object.args[1]),
                         Command("Jmp", Argument("lnk", "^cycle_begin")),
                         Mark("#cycle_end")]
        commands += [Command("Psh", Argument("lnk", "^rubbish"))]
    elif yo_object.group == "program":
        for child in yo_object.args:
            commands += [*get_vir_commands(child),
                         Command("Pop", Argument("lnk", "^rubbish"))]
    return commands


def get_abs_addresses(program):
    links = []
    for command in program.commands:
        if isinstance(command, Command):
            args = list(filter(lambda arg: arg.arg_type == "lnk",
                               command.args))
            links += args
        elif isinstance(command, Mark):
            links += [command]
    print(*links, sep="\n")
    for i in range(len(links)):
        link_analize(links, i)


def link_analize(links, link_number):
    link = links[link_number]
    link_sign = link.value[:1]
    link_name = link.value[1:]
    if link_sign == "#":
        return
    if link_name in special_links:
        pass
    else:
        if link_sign == "^":
            pass
        elif link_sign == "*":
            pass


if __name__ == '__main__':
    file = input()
    with open(f"{file}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    print(result[0])
    program = Program([])
    commands = get_vir_commands(result[0])
    for command in commands:
        program.add(command)
    print(program)
    get_abs_addresses(program)
