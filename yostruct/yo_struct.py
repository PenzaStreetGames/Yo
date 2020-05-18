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


class Node:
    """Узел дерева тегов"""

    def __init__(self, name, parent, stage="tag_named"):
        self.name = name
        self.parent = parent
        self.kind = "single"
        self.indent = 0
        self.children = []
        self.attributes = {}
        self.stage = stage
        # "tag_named" -> "attributes_opened" -> "attributes_closed" ->
        # -> "children_opened" -> "closed"

    def add_children(self, node):
        self.children.append(node)
        node.parent = self

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_indent(self, indent):
        self.indent = indent

    def to_html(self):
        if self.kind == "single":
            pass


class BaseYoStructException(Exception):
    """Базовая ошибка YoStruct"""


class StructSyntaxError(BaseYoStructException):
    """Синтаксическая ошибка YoStruct"""


def syntax_analise(tokens):
    """Осмысление потока токенов и создание дерева"""
    root = Node("!root", None, stage="children_opened")
    stack = [root]
    for token in tokens:
        target = stack[-1]
        parent = target.parent
        if target.stage == "tag_named":
            pass
        elif target.stage == "attributes_opened":
            pass
        elif target.stage == "attributes_closed":
            pass
        elif target.stage == "children_opened":
            pass
        elif target.stage == "closed":
            pass
        else:
            raise StructSyntaxError(
                f"Неизвестное состояние тега {target.name}: {target.stage}")



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
