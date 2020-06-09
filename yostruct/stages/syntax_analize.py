from yostruct.classes.root import Root
from yostruct.classes.fork import Fork
from yostruct.classes.leaf import Leaf
from yostruct.classes.comment import Comment
from yostruct.errors import StructSyntaxError


def syntax_analise(tokens):
    """Осмысление потока токенов и создание дерева"""
    root = Root()
    stack = [root]
    indent = 0
    for token in tokens:
        node = stack[-1]
        parent = node.parent
        line = token.line
        if node.state == "root_open":
            if token.category == "comment":
                Comment(token.name, node)
                node.state = "root_value"
            elif token.category == "string":
                Leaf(token.name, node)
                node.state = "root_value"
            elif token.name == "pass":
                node.state = "root_value"
            elif token.category == "name":
                fork = Fork(token.name, node)
                node.state = "root_value"
                stack.append(fork)
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "root_value":
            if token.category == ",":
                node.state = "root_open"
            elif token.name == "\n":
                node.state = "root_open"
            elif token.category == "space":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "tag_open":
            if token.name == "(":
                node.state = "property_open"
                node.properties = {}
            elif token.name == ":":
                node.state = "oneline_open"
                node.properties = {}
                node.children = []
            elif token.name == "{":
                if node.parent.state in {"scope_value", "root_value"}:
                    node.state = "scope_open"
                    node.properties = {}
                    node.children = []
                else:
                    raise StructSyntaxError("Скобочные теги могут храниться "
                                            "только внутри скобочных тегов.")
            elif token.name == ",":
                node.state = "tag_closed"
                stack.pop()
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_open"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\",\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            elif token.name == "\n":
                node.state = "tag_closed"
                stack.pop()
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_open"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\"\\n\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            elif token.category == "space":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "property_open":
            if token.category == "name":
                node.state = "property_key"
                node.properties[token.name] = True
            elif token.name == ")":
                node.state = "property_close"
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "property_key":
            if token.name == "=":
                node.state = "property_equal"
            elif token.name == ",":
                node.state = "property_open"
            elif token.name == ")":
                node.state = "property_close"
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "property_equal":
            if token.category == "string":
                node.state = "property_value"
                for key, value in node.properties.items():
                    if value is None:
                        node.properties[key] = token.name
                        break
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "property_value":
            if token.name == ")":
                node.state = "property_close"
            elif token.name == ",":
                node.state = "property_open"
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "property_close":
            if token.name == ":":
                node.state = "oneline_open"
                node.children = []
            elif token.name == "{":
                if node.parent.state in {"scope_value", "root_value"}:
                    node.state = "scope_open"
                    node.children = []
                else:
                    raise StructSyntaxError("Скобочные теги могут храниться "
                                            "только внутри скобочных тегов.")
            elif token.name == ",":
                node.state = "tag_closed"
                stack.pop()
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_open"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\",\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            elif token.name == "\n":
                node.state = "tag_closed"
                stack.pop()
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_newline"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\"\\n\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            elif token.category == "space":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "oneline_open":
            if token.category == "string":
                node.state = "oneline_close"
                Leaf(token.name, node)
                stack.pop()
            elif token.name == "pass":
                node.state = "oneline_close"
                stack.pop()
            elif token.category == "name":
                fork = Fork(token.name, node)
                node.state = "oneline_close"
                stack.append(fork)
            elif token.category == "space":
                pass
            elif token.name == "\n":
                if node.parent.state in {"indent_value", "root_value"}:
                    node.state = "indent_newline"
                else:
                    raise StructSyntaxError("Отступные теги могут храниться"
                                            "только внутри отступных тегов.")
            else:
                invalid_token(node, token)
        elif node.state == "oneline_close":
            if token.name == ",":
                while node.state == "oneline_close":
                    stack.pop()
                    node = stack[-1]
                    parent = node.parent
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_open"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\"\\n\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            elif token.name == "\n":
                while node.state == "oneline_close":
                    stack.pop()
                    node = stack[-1]
                    parent = node.parent
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_newline"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\"\\n\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            else:
                invalid_token(node, token)
        elif node.state == "indent_newline":
            if token.category == "space":
                indent = len(token.name)
                if indent > node.indent:
                    node.inside_indent = indent
                    node.state = "indent_open"
                else:
                    while node.state in {"indent_newline", "indent_value"} and \
                            indent <= node.indent:
                        node.state = "indent_close"
                        stack.pop()
                        node = node.parent
                    node.state = "indent_open"
            elif token.category == "name":
                indent = 0
                while node.state in {"indent_newline", "indent_value"} and \
                        indent <= node.indent:
                    node.state = "indent_close"
                    stack.pop()
                    node = node.parent
                node.state = "root_value"
                if token.name != "pass":
                    fork = Fork(token.category, node)
                    stack.append(fork)
            elif token.category == "string":
                indent = 0
                while node.state in {"indent_newline", "indent_value"} and \
                        indent <= node.indent:
                    node.state = "indent_close"
                    stack.pop()
                    node = node.parent
                node.state = "root_value"
                Leaf(token.name, node)
            elif token.category == "comment":
                indent = 0
                while node.state in {"indent_newline", "indent_value"} and \
                        indent <= node.indent:
                    node.state = "indent_close"
                    stack.pop()
                    node = node.parent
                node.state = "root_value"
                Comment(token.name, node)
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "indent_open":
            if token.name == "pass":
                node.state = "indent_value"
            elif token.category == "string":
                node.state = "indent_value"
                Leaf(token.name, node)
            elif token.category == "name":
                fork = Fork(token.name, node)
                node.state = "indent_value"
                stack.append(fork)
            elif token.category == "comment":
                node.state = "indent_value"
                Comment(token.name, node)
            elif token.category == "space":
                pass
            elif token.name == "\n":
                node.state = "indent_newline"
            else:
                invalid_token(node, token)
        elif node.state == "indent_value":
            if token.name == ",":
                node.state = "indent_open"
            elif token.name == "\n":
                node.state = "indent_newline"
            elif token.category == "space":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "scope_open":
            if token.category == "string":
                Leaf(token.name, node)
                node.state = "scope_value"
            elif token.category == "name" and token.name != "pass":
                fork = Fork(token.name, node)
                node.state = "scope_value"
                stack.append(fork)
            elif token.name == "}":
                node.state = "scope_close"
            elif token.category == "comment":
                node.state = "scope_open"
                Comment(token.name, node)
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "scope_value":
            if token.name == ",":
                node.state = "scope_open"
            elif token.name == "}":
                node.state = "scope_close"

            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "scope_close":
            if token.name == ",":
                node.state = "tag_closed"
                stack.pop()
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_open"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\",\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
            elif token.name == "\n":
                node.state = "tag_closed"
                stack.pop()
                if parent.name == "!root":
                    parent.state = "root_open"
                elif parent.state == "indent_value":
                    parent.state = "indent_open"
                elif parent.state == "scope_value":
                    parent.state = "scope_open"
                else:
                    raise StructSyntaxError(f"\"\\n\" в теге {parent.name} "
                                            f"в состоянии {parent.state}")
        else:
            invalid_state(node, token)
    return root


def invalid_token(node, token):
    raise StructSyntaxError(f"Неправильный токен: \"{token.name}\" в "
                            f"{node.state}. Строчка: {token.line}")


def invalid_state(node, token):
    raise StructSyntaxError(f"Неправильное состояние тега {node.name}: "
                            f"{node.state}. Строчка: {token.line}")
