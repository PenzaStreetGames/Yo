from yostruct.classes.node import Node
from yostruct.errors import HTMLTrasformError, StructBuildError


class Root(Node):
    """Корень структуры"""

    def __init__(self):
        super().__init__(name="!root", parent=None, state="root_open",
                         properties={}, children=[], indent=-1)

    def add_children(self, child):
        if self.children is not None:
            self.children.append(child)
            child.set_parent(self)
        else:
            raise StructBuildError(f"Попытка добавить дочерний элемент в "
                                   f"{self.name}")

    def to_html_attributes(self):
        return ""

    def to_html_children(self, style="pretty"):
        children_code = []
        for child in self.children:
            children_code.append(child.to_html(style=style))
        if style == "pretty" or style == "rich":
            children_code = "\n".join(children_code)
        elif style == "oneline":
            children_code = " ".join(children_code)
        else:
            raise HTMLTrasformError(f"Неизвестный стиль обработки html {style}")
        return children_code

    def to_html(self, style="pretty"):
        code = ""
        children_code = self.to_html_children(style=style)
        if style in {"pretty", "oneline", "rich"}:
            code = f"{children_code}"
        else:
            raise HTMLTrasformError(
                f"Неизвестный стиль обработки html {style}")
        return code

    def __str__(self):
        if self.children:
            children = "\n".join(map(str, self.children))
            children = children.replace("\n", "\n    ")
            res = f"{self.name} {self.properties}:\n    {children}"
        else:
            res = f"{self.name} {self.properties}"
        return res
