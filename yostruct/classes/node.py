class Node:
    """Родоначальник семейства узлов"""

    def __init__(self, name, parent, state="tag_open", properties={},
                 children=None, indent=0):
        self.name = name
        self.parent = parent
        if parent is not None:
            self.parent.add_children(self)
            self.indent = parent.inside_indent
        else:
            self.indent = indent
        self.inside_indent = indent + 1
        self.state = state
        self.properties = properties
        self.children = children

    def set_parent(self, parent):
        pass

    def add_children(self, child):
        pass

    def to_html_attributes(self):
        pass

    def to_html_children(self, style="pretty"):
        pass

    def to_html(self, style="pretty"):
        pass

    def __str__(self):
        return ""

    def __repr__(self):
        return f"{self.name} {self.state}"
