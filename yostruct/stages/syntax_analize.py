from yostruct.classes.node import Node
from yostruct.classes.root import Root
from yostruct.classes.fork import Fork
from yostruct.classes.leaf import Leaf
from yostruct.classes.comment import Comment
from yostruct.errors.errors import StructSyntaxError


def syntax_analise(tokens):
    """Осмысление потока токенов и создание дерева"""
    root = Root()
    stack = [root]
    indent = 0
    for token in tokens:
        node = stack[-1]
        parent = node.parent
        if node.state == "root_indent":
            if token.category == "comment":
                Comment(token.name, node)
                node.state = "root_comment"
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
                node.inside_indent = len(token.name)
                node.state = "root_open"
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "root_open":
            if token.category == "comment":
                Comment(token.name, node)
                node.state = "root_comment"
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
            elif token.category == "\n":
                node.state = "root_indent"
            elif token.category == "space":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "tag_open":
            if token.name == "(":
                node.state = "property_open"
            elif token.name == ":":
                node.state = "oneline_open"
                node.properties = {}
            elif token.name == "{":
                node.state = "scope_open"
                node.properties = {}
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
            else:
                invalid_token(node, token)
        elif node.state == "property_open":
            if token.category == "name" and token.name != "pass":
                node.state = "property_key"
                node.properties[token.name] = None
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
            elif token.category == "space":
                pass
            elif token.name == "\n":
                pass
            else:
                invalid_token(node, token)
        elif node.state == "property_equal":
            if token.category == "string" or token.name == "true":
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
        elif node.state == "property_close":
            if token.name == ":":
                node.state = "oneline_open"
            elif token.name == "{":
                node.state = "scope_open"
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
            else:
                invalid_token(node, token)
        elif node.state == "oneline_open":
            pass


def invalid_token(node, token):
    raise StructSyntaxError(f"Неправильный токен: {token.name} в {node.state}."
                            f"Строчка: {token.line}")
