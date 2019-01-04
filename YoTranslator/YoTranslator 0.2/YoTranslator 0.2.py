key_words = ["while", "if"]
structure_words = ["while", "if"]
functions = ["print"]
signs = ["=", "[", "]", "<", ">", ":", "+", "(", ")", ","]
space, empty = " ", ""
special_symbols = {"command_end": "*ce",
                   "indent": "*i",
                   "line_indent": "*i{}"}


class Object:
    def __init__(self, parent, func, args, index):
        self.parent = parent
        self.func = func
        self.args = args
        self.index = index


def translate(program):

    def add_word():
        global word, tokens
        if word != empty:
            tokens += [word]
        word = ""

    pre_categoty = ""
    for symbol in program:
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

    return program


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        result = translate(infile.read())
    print(result)
