from yostruct.classes.node import Node


class Comment(Node):
    """Комментарий структуры"""

    def __init__(self, name, parent, indent=0):
        super().__init__(name=name, parent=parent, state="comment",
                         properties={}, children=[], indent=indent)

    def to_html_attributes(self):
        return ""

    def to_html_children(self, style="pretty"):
        return ""

    def to_html(self, style="pretty"):
        return f"<!--{self.name}-->"

    def __str__(self):
        return self.name
