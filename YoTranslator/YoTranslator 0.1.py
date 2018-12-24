key_words = ["while", "if", "print"]
signs = ["=", "[", "]", "<", ">", ":", "+", "(", ")", ","]
space, empty = " ", ""
special_symbols = {"command_end": "*ce",
                   "indent": "*i"}

tokens = []
pre_symbol = ""
word = ""

commands = []
pre_indent = 0

class TokenError(Exception):
    pass


def token_split(text):
    global tokens, pre_symbol, word

    def add_word():
        global word, tokens
        if word != empty:
            tokens += [word]
        word = ""

    for symbol in text:
        if symbol == "\n" or symbol == "\r":
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


def command_split():
    pass


if __name__ == '__main__':
    with open(f"{input()}.yotext", "r", encoding="utf-8") as infile:
        text = token_split(infile.read())
        print(text)
