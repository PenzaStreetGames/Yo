"""
YoStruct - часть проекта Yo. Занимается преобразованием псевдоструктур в html
и xml в общности.
"""

from yostruct.stages.token_split import token_split
from yostruct.stages.syntax_analize import syntax_analise
from yostruct.stages.build_html import build_html
from yostruct.errors import StructSyntaxError


def build_tree(text):
    """Построение дерева тегов"""
    tokens = token_split(text)
    tree = syntax_analise(tokens)
    return tree


def convert_yostruct(text, style="pretty"):
    """Поэтапное преобразование"""
    tokens = token_split(text)
    tree = syntax_analise(tokens)
    html = build_html(tree, style=style)
    return html


if __name__ == '__main__':
    """Сначала файл считывается, преобразуется в дерево тегов, затем в html"""
    file = "example"
    with open(f"{file}.yostruct", "r", encoding="utf-8") as infile:
        structure_text = infile.read()
        lines = structure_text.split("\n")
    tokens = token_split(structure_text, debug=True)
    # print("\n".join(map(str, tokens)))
    try:
        tree = syntax_analise(tokens)
    except StructSyntaxError as error:
        print(error)
        number = str(error).split()[-1]
        print(f"{number} {lines[int(number) - 1]}")
        tree = []
    # print(tree)
    html = build_html(tree, style="oneline")
    print(html)
    with open(f"{file}.html", "w", encoding="utf-8") as outfile:
        outfile.write(html)
    """file = input("Введите название файла без расширения")
    with open(f"{file}.yostruct", "r", encoding="utf-8") as infile:
        structure_text = infile.read()
    tree = build_tree(structure_text)
    html = to_html(tree)
    with open(f"{file}.html") as outfile:
        outfile.write(html)"""
