"""
YoStruct - часть проекта Yo. Занимается преобразованием псевдоструктур в html
и xml в общности.
"""


def build_tree(text):
    """Построение дерева тегов"""
    tokens = token_split(text)
    tree = syntax_analise(tokens)
    return tree


def token_split(text, debug=False):
    """Разбиение текста на токены"""
    signs = "():{},\n=\"\'\\`"
    tokens = []
    word = ""
    category = "space"
    quote, quote_type = False, ""
    unexpected = {}
    for symbol in text:
        if symbol in {"\'", "\"", "`"}:
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
    return tokens


def syntax_analise(tokens):
    """Осмысление потока токенов и создание дерева"""


def to_html(tree):
    """Преобразование дерева в html-текст"""
    pass


if __name__ == '__main__':
    """Сначала файл считывается, преобразуется в дерево тегов, затем в html"""
    file = "example"
    with open(f"{file}.yostruct", "r", encoding="utf-8") as infile:
        structure_text = infile.read()
    tokens = token_split(structure_text, debug=True)
    print("\n".join(map(lambda token: f"'{token}'" if token != "\n" else "'\\n'", tokens)))
    """file = input("Введите название файла без расширения")
    with open(f"{file}.yostruct", "r", encoding="utf-8") as infile:
        structure_text = infile.read()
    tree = build_tree(structure_text)
    html = to_html(tree)
    with open(f"{file}.html") as outfile:
        outfile.write(html)"""
