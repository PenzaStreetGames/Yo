def syntax_analise(tokens):
    """Осмысление потока токенов и создание дерева"""
    root = Node("!root", None, stage="children_opened", indent=-1)
    stack = [root]
    indent = 0
    prev_token = None
    for token in tokens:
        target = stack[-1]
        parent = target.parent
        if target.stage == "tag_named":
            pass
        elif target.stage == "attributes_opened":
            pass
        elif target.stage == "attributes_closed":
            pass
        elif target.stage == "children_opened":
            if prev_token == "\n":
                indent = len(token) if token[0] == " " else 0
                while indent <= target.indent and target.kind == "double_indent":
                    target.stage = "closed"
                    stack.pop()
                    target = parent
                    parent = target.parent
            if token[0].isalpha():
                new_node = Node(token, target, indent=indent)
                stack.append(new_node)
            elif token[0] in {"\'", "\"", "`"} or token[0].isalpha():
                new_node = Content(token, target)
            elif token[0] == " " and prev_token == "\n":
                indent = len(token)
            elif token == "}":
                if target.kind == "double_scope":
                    target.stage = "closed"
                    stack.pop()
                    target = parent
                    parent = target.parent
                else:
                    raise StructSyntaxError(f"Неожиданный символ: {token}")
            elif token == "\n":
                pass
                while target.kind == "double_one_line":
                    pass
            elif token == ",":
                pass

        elif target.stage == "closed":
            pass
        else:
            raise StructSyntaxError(
                f"Неизвестное состояние тега {target.name}: {target.stage}")
        prev_token = token
