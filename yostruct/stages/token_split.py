from yostruct.classes.token import Token


def token_split(text, debug=False):
    """Разбиение текста на токены"""
    signs = "():{},\n=\"\'\\`"
    tokens = []
    word = ""
    category = "space"
    quote, quote_type = False, ""
    comment, comment_type = False, ""
    unexpected = {}
    for symbol in text:
        if symbol == "#":
            if not quote:
                tokens.append(word)
                comment = True
                comment_type = "one_line"
                category = "comment"
                word = symbol
            else:
                word += symbol
        elif comment:
            if symbol != "\n":
                word += symbol
            else:
                comment = False
                tokens.append(word)
                category = "signs"
                word = symbol
        elif symbol in {"\'", "\"", "`"}:
            if not quote:
                tokens.append(word)
                quote = True
                quote_type = symbol
                category = "string"
                word = symbol
            elif symbol != quote_type:
                word += symbol
            elif word[-1] == "\\":
                word += symbol
            else:
                quote = False
                word += symbol
        elif quote:
            word += symbol
        elif symbol == " ":
            if category != "space":
                tokens.append(word)
                category = "space"
                word = symbol
            else:
                word += symbol
        elif symbol in signs:
            tokens.append(word)
            word = symbol
            category = "signs"
        elif symbol.isalpha():
            if category != "word":
                tokens.append(word)
                category = "word"
                word = symbol
            else:
                word += symbol
        elif symbol.isdigit():
            if category != "digit":
                tokens.append(word)
                category = "digit"
                word = symbol
            else:
                word += symbol
        else:
            unexpected[symbol] = unexpected.get(symbol, 0) + 1
    if debug:
        if len(unexpected.keys()) != 0:
            print("Неожидаемые символы:")
            for key, value in unexpected.items():
                print(f'"{key}":', value)
    if tokens:
        tokens.pop(0)
    return tokens
