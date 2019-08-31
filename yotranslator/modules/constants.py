import json
with open("modules/basic.yolp", "r", encoding="utf8") as file:
    yolp_basic = json.loads(file.read())


key_words = ["while", "if", "else", "elseif", "break", "continue", "none",
             "true", "false", "not", "and", "or", "xor", "pass"]
functions = ["print", "input", "len"]
signs = ["=", "[", "]", "(", ")", "{", "}", ",", ";", ":", "+", "-", "*", "/",
         "%", ">", "<", "?"]
sign_combos = ["=?"]
quotes = ["'", '"']
comment = "#"
space, empty = " ", ""
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
    "interrupt_words": ["break", "continue", "pass"],
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
            "continue": 1,
            "pass": 1
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
            "continue": "no",
            "pass": "no"
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
    "cmd": 1,
    "lnk": 1,
    "log": 1,
    "num": 1,
    "str": "many",
    "lst": 1
}
# специальные ссылки
special_links = ["next_branch", "branch_begin", "branching_end",
                 "cycle_begin", "cycle_end", "rubbish"]
# нумерация бинарных объектов
binary_values = {
    "types":
        {
            "non": 0,
            "lnk": 1,
            "cmd": 2,
            "log": 3,
            "num": 4,
            "str": 5,
            "lst": 6
        },
    "commands":
        {
            "End": 0, "Jmp": 1, "Jif": 2, "Crt": 3, "Fnd": 4,
            "Eqt": 5, "Len": 6, "Sob": 7, "Inp": 8, "Out": 9,
            "Psh": 10, "Pop": 11, "Cal": 12, "Ret": 13, "Not": 14,
            "And": 15, "Or": 16, "Xor": 17, "Neg": 18, "Add": 19,
            "Inc": 20, "Dcr": 21, "Sub": 22, "Mul": 23, "Div": 24,
            "Mod": 25, "Eql": 26, "Grt": 27, "Les": 28, "Nop": 29
        }
}
# представление типа в памяти
type_memory_view = {
    "number": ["non", "cmd", "lnk", "log", "num", "lst"],
    # тип списка является флагом
    "symbol_list": ["str"]
}

highlight_groups = [
    "non colored",
    "comment",
    "sign",
    "logic_value",
    "logic_operation",
    "number",
    "string",
    "object",
    "built_in_function",
    "structure"
]
highlight_tokens = {
    "non colored": [],
    "comment": [],
    "sign": [],
    "logic_value": [],
    "logic_operation": [],
    "number": [],
    "string": [],
    "object": [],
    "built_in_function": [],
    "structure": []
}
