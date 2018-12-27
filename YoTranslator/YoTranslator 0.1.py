key_words = ["while", "if"]
functions = ["print"]
signs = ["=", "[", "]", "<", ">", ":", "+", "(", ")", ","]
space, empty = " ", ""
special_symbols = {"command_end": "*ce",
                   "indent": "*i",
                   "line_indent": "*i{}"}

# for token_split
tokens = []
pre_symbol = ""
word = ""

# for command_split
commands = []
pre_indent = 0
command = []
pre_token = ""

# for token_analise
pre_group = ""

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
    "key_word": 10
}

priority = {

}

class TokenError(Exception):
    pass


class Token:
    def __init__(self, name, group):
        self.name = name
        self.group = group

    def token_analyse(self):
        pass

    def __str__(self):
        return f"{self.group} \"{self.name}\""

    def __repr__(self):
        return f"{self.group} \"{self.name}\""


def token_split(text):
    global tokens, pre_symbol, word

    def add_word():
        global word, tokens
        if word != empty:
            tokens += [word]
        word = ""

    for symbol in text:
        if symbol == "\n" or symbol == "\r":
            if word != special_symbols["command_end"]:
                add_word()
                pre_symbol = "sign"
                word = special_symbols["command_end"]
        elif symbol == space:
            if word == special_symbols["command_end"]:
                add_word()
                word = special_symbols["indent"]
                pre_symbol = "sign"
            elif word == special_symbols["indent"]:
                add_word()
                word = special_symbols["indent"]
                pre_symbol = "sign"
            elif pre_symbol != space:
                add_word()
                pre_symbol = "space"
            else:
                pass
        elif symbol in signs:
            add_word()
            pre_symbol = "sign"
            word += symbol
        elif symbol.isalpha():
            if pre_symbol == "sign":
                add_word()
            pre_symbol = "alpha"
            word += symbol
        elif symbol.isdigit():
            if pre_symbol == "sign":
                add_word()
            pre_symbol = "digit"
            word += symbol
        else:
            raise TokenError(f"Неизвестный символ {symbol}")
    add_word()
    return tokens


def command_split(tokens):
    global commands, command, pre_token, pre_indent

    def add_command():
        global command, commands
        if command:
            commands += [command]
        command = []

    for token in tokens:
        if token == special_symbols["indent"]:
            if pre_token == special_symbols["indent"]:
                pre_indent += 1
            elif pre_token == special_symbols["command_end"]:
                pre_indent = 0
                pre_indent += 1
            pre_token = special_symbols["indent"]
        elif token == special_symbols["command_end"]:
            add_command()
            pre_token = special_symbols["command_end"]
            pre_indent = 0
        else:
            if pre_token == special_symbols["indent"]:
                command += [special_symbols["line_indent"].format(pre_indent)]
            elif pre_token == special_symbols["command_end"]:
                command += [special_symbols["line_indent"].format(pre_indent)]
            elif pre_token == empty:
                command += [special_symbols["line_indent"].format(pre_indent)]
            command += [token]
            pre_token = token
    add_command()
    return commands

def token_analise(out_commands):
    global commands

    result = []
    for command in commands:
        result += [[]]
        for token in command:
            group = ""
            if token.startswith(special_symbols["indent"]):
                pass
            elif token.isdigit():
                group = "object"
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
                    else:
                        group = "sub_object"
                elif token == "]":
                    group = "sub_object"
                elif token == "(":
                    if pre_group != "object":
                        group = "brackets"
                    else:
                        group = "call"
                elif token == ")":
                    group = "call"
                elif token == ",":
                    group = "brackets"
            elif token in key_words:
                group = "key_word"
            elif token[0].isalpha():
                group = "object"
            else:
                raise TokenError(f"Неизвестный токен {token}")
            token = Token(token, group)
            result[-1] += [token]
            pre_group = group
    commands = result.copy()

    return result


def command_analise():
    pass


def expression_analise():
    pass


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        stage_1 = token_split(infile.read())
    print(stage_1)
    stage_2 = command_split(stage_1)
    print(stage_2)
    stage_3 = token_analise(stage_2)
    print(stage_3)
