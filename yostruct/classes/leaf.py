from yostruct.classes.node import Node


class Leaf(Node):
    """Лист структуры"""

    def __init__(self, name, parent, indent=0):
        super().__init__(name=name, parent=parent, state="leaf",
                         properties={}, children=[], indent=indent)

    def to_html_attributes(self):
        return ""

    def to_html_children(self, style="pretty"):
        return ""

    def to_html(self, style="pretty"):
        return self.name[1:-1]

    def __str__(self):
        return self.name
