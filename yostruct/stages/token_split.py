from yostruct.classes.token import Token


def token_split(text, debug=False):
    """Разбиение текста на токены"""
    signs = "():{},\n=\"\'\\`"
    tokens = []
    line = 1
    token = Token(" ", "space", 1)
    unexpected = {}
    text += "\n"
    for symbol in text:
        if symbol == "#":
            if not token.quote:
                tokens.append(token)
                token = Token(symbol, "comment", line)
            else:
                token.add_symbol(symbol)
        elif token.comment:
            if symbol != "\n":
                token.add_symbol(symbol)
            else:
                tokens.append(token)
                token = Token(symbol, "signs", line)
                line += 1
        elif symbol in {"\'", "\"", "`"}:
            if not token.quote:
                tokens.append(token)
                token = Token(symbol, "string", line)
            elif symbol != token.quote_type:
                token.add_symbol(symbol)
            elif token.name == "\\":
                token.add_symbol(symbol)
            else:
                token.quote = False
                token.add_symbol(symbol)
        elif token.quote:
            token.add_symbol(symbol)
        elif symbol == " ":
            if token.category != "space":
                tokens.append(token)
                token = Token(symbol, "space", line)
            else:
                token.add_symbol(symbol)
        elif symbol == "\n":
            tokens.append(token)
            token = Token(symbol, "sign", line)
            line += 1
        elif symbol in signs:
            tokens.append(token)
            token = Token(symbol, "sign", line)
        elif symbol.isalpha():
            if token.category != "name":
                tokens.append(token)
                token = Token(symbol, "name", line)
            else:
                token.add_symbol(symbol)
        elif symbol.isdigit():
            if token.category not in {"digit", "name"}:
                tokens.append(token)
                token = Token(symbol, "digit", line)
            else:
                token.add_symbol(symbol)
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
