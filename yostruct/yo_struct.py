"""
YoStruct - часть проекта Yo. Занимается преобразованием псевдоструктур в html
и xml в общности.
"""
from yostruct.classes.node import Node
from yostruct.classes.root import Root
from yostruct.classes.fork import Fork
from yostruct.classes.leaf import Leaf

from yostruct.stages.token_split import token_split
from yostruct.stages.syntax_analize import syntax_analise
from yostruct.stages.build_html import build_html

def build_tree(text):
    """Построение дерева тегов"""
    tokens = token_split(text)
    tree = syntax_analise(tokens)
    return tree

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
