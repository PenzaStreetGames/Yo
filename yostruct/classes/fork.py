from yostruct.classes.node import Node
from yostruct.errors import HTMLTrasformError, StructBuildError


class Fork(Node):
    """Родоначальник семейства узлов"""

    def __init__(self, name, parent, state="tag_open"):
        super().__init__(name=name, parent=parent, state=state)

    def set_parent(self, parent):
        self.parent = parent

    def add_children(self, child):
        if self.children is not None:
            self.children.append(child)
            child.set_parent(self)
        else:
            raise StructBuildError(f"Попытка добавить дочерний элемент в "
                                   f"{self.name}")

    def to_html_attributes(self):
        attributes_code = []
        for attribute, value in self.properties.items():
            if value is True:
                attributes_code.append(f"{attribute}")
            else:
                attributes_code.append(f"{attribute}={value}")
        attributes_code = " ".join(attributes_code)
        return attributes_code

    def to_html_children(self, style="pretty"):
        children_code = []
        for child in self.children:
            children_code.append(child.to_html())
        if style == "pretty":
            children_code = "\n".join(children_code)
        elif style == "oneline":
            children_code = " ".join(children_code)
        else:
            raise HTMLTrasformError(f"Неизвестный стиль обработки html {style}")
        return children_code

    def to_html(self, style="pretty"):
        code = ""
        attributes_code = self.to_html_attributes()
        if self.children is None:
            if attributes_code:
                code = f"<{self.name} {attributes_code}/>"
            else:
                code = f"<{self.name}/>"
        else:
            if attributes_code:
                code = f"<{self.name} {attributes_code}>"
            else:
                code = f"<{self.name}>"
            children_code = self.to_html_children(style=style)
            if style == "pretty":
                children_code = children_code.replace("\n", "\n    ")
                code = f"{code}\n    {children_code}\n</{self.name}>"
            elif style == "oneline":
                code = f"{code} {children_code} </{self.name}>"
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
