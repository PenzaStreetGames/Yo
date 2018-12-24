key_words = ["while", "if", "print"]
signs = ["=", "[", "]", "<", ">", ":", "+", "(", ")", ","]
space, empty = " ", ""


def token_split(text):
    tokens = []
    pre_symbol = ""
    word = ""

    def add_word():
        global word, tokens
        if word != empty:
            tokens += [word]
        word = ""

    for symbol in text:
        if symbol == space:
            if pre_symbol != space:
                add_word()
