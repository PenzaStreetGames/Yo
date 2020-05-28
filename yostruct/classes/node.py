class Node:
    """Родоначальник семейства узлов"""

    def __init__(self, name, parent, state="tag_open", properties={},
                 children=None, indent=0):
        self.name = name
        self.parent = parent
        if parent is not None:
            self.parent.add_children(self)
        self.state = state
        self.properties = properties
        self.children = children
        self.indent = indent

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
